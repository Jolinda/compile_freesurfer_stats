# compile_freesurfer_stats
A python script that can be used instead of aparcstats2table/asegstats2table. More flexible and a good deal faster.

To use, specify the path to your freesurfer results, which stats file to extract measurements from, and what type of measurement to extract. For example, to extract volume measurements from the aseg.stats file for all subjects in the directory, you would use:

`python compile_freesurfer_stats.py -f <freesurfer_output> -s aseg.stats -o aseg.csv -m Volume_mm3`

The script will also extract any lines in the stats file that begin with # Measure.

You can specify an input file with a list of subjects to extract, or a glob to only match certain subjects:

`python compile_freesurfer_stats.py -f <freesurfer_output> -s rh.aparc.stats -o rh_aparc_surf.csv -m SurfArea -i subjects.txt`
`python compile_freesurfer_stats.py -f <freesurfer_output> -s rh.aparc.stats -o rh_aparc_surf.csv -m SurfArea -g *long*`

If you'd like to add a prefix and/or postfix to the column names:
 
`python compile_freesurfer_stats.py -f <freesurfer_output> -s rh.aparc.stats -o rh_aparc_thick.csv -m ThickAvg --prefix RH_ --postfix _thickness`
