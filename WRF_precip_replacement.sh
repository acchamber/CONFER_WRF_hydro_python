#!/bin/bash
set -eu

# script to regrid all IMERG.nc4 files in a folder to the first gridspec in another file
# intended use is to put IMERG data on WRF output grid - must have grid explicitly defined (not "generic").
# Can check above with the cdo sinfon command - must have cdo in your current enviroment

# input folders and input file are defined in the command line - output is in same locations

# start and end date are inclusive, defined on call 

# example run - WRF_precip_replacement.sh ~/path/to/IMERG_data grid_file.nc ~/path/to/wrfout_data 2011_01_01 2011_02_01

# reccomended not to run in more than monthly chunks

imerg_folder=$1 
grid_file=$2
wrfout_folder=$3
start_date=$4
end_date=$5 

#create template file

cdo griddes $grid_file >  temp.txt
python WRF_precip.py strip_grid_file temp.txt 
rm temp.txt

# regrid all IMERG data to template - creates lots of terminal text
filenames=$(ls $imerg_folder/*IMERG*.nc4)
for file in $filenames
do
    cdo remapbil,gridfile.txt $file ${file}.rg 
done


# run the python functions doing the meat of the work replacing rainfall with IMERG
python WRF_precip.py imerg_to_wrfout $imerg_folder $wrfout_folder $start_date $end_date 

