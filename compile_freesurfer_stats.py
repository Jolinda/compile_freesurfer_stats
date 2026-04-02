import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import sys

def main(args=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='freesurfer subjects directory', required=True)
    parser.add_argument('-s', '--statsfile', help='stats file to parse, eg lh.aparc.stats', required=True)
    parser.add_argument('-i', '--input_file', help='textfile with list of subjects to extract', default=None)
    parser.add_argument('-g', '--glob', help='pattern to match for subjects', default='*')
    parser.add_argument('-c', '--column', help='column to extract, eg Volume_mm3, ThickAvg, SurfArea', required=False)
    parser.add_argument('-o', '--output', help='output file name', required=True)
    parser.add_argument('--prefix', help='prefix for stats header names', default='')
    parser.add_argument('--postfix', help='postfix for stats header names', default='')
    parser.add_argument('--no-measures', action='store_false', help='do not include #Measure lines', dest='measures')   

    args=parser.parse_args()
    input_type = args.statsfile
    output_file = args.output
    column = args.column
    glob = args.glob
    prefix = args.prefix
    postfix = args.postfix
    input_file = args.input_file
    include_measures = args.measures

    if input_file and glob != '*':
        sys.exit('You cannot use an input file and a glob. Pick one.')

    # path to freesurfer results
    datapath = Path(args.directory)

    if not datapath.exists():
        sys.exit(f'{datapath} not found')

    records = []

    cols_to_rename = None

    if input_file:
        filelist = [datapath/x/'stats'/input_type for x in Path(input_file).read_text().splitlines()]
    else:
        filelist = datapath.glob(f'{glob}/stats/{input_type}')

    # for every matching file
    for stats_file in filelist:
        if not stats_file.exists():
            print(f'{stats_file} not found')
            continue

        # start a new record
        record={'subject':stats_file.parts[-3]}

        # read the file
        stats_text = stats_file.read_text().splitlines()

        # get the column headers
        header_line = next((x for x in stats_text if 'ColHeaders' in x), None)

        if header_line:
            col_headers=header_line.split()[2:]
            if not column:
                sys.exit(f'You must specify a measurement to extract for this file. Choices are: {col_headers[1:]}')
            if column not in col_headers:
                sys.exit(f'{column} measurement not found. Choices are: {col_headers[1:]}')

            # read the stats & add them to the record
            stats_df = pd.read_csv(stats_file, comment='#', names=col_headers, delimiter=' ', skipinitialspace=True, 
                                   index_col='StructName', usecols=range(0,len(col_headers)))

            # first time through, save the column names
            if (prefix or postfix) and not cols_to_rename:
                cols_to_rename = list(stats_df.index)
            record.update(stats_df[column].to_dict())

        # add any # Measures to the record
        if include_measures:
            measures={x.split(',')[1].strip():float(x.split(',')[-2].strip()) for x in stats_text if '# Measure' in x}
            record.update(measures)

        # add record to list of records
        records.append(record)

    # convert list of records to dataframe and save to output
    df = pd.DataFrame.from_records(records)
    if cols_to_rename:
        df.rename(columns=dict(zip(cols_to_rename, [f'{prefix}{x}{postfix}' for x in cols_to_rename])), inplace=True)
    df.sort_values(by='subject', inplace=True)
    df.to_csv(output_file, index=False)
    print('finished')

if __name__ == "__main__":
    main()
