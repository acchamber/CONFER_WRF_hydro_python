import netCDF4
import numpy as np
import sys
import glob
import datetime
import iris

def strip_grid_file(file):
    ''' Takes in filepath as string, opens, and writes txt between 3rd and 4th # to gridfile.txt. 
    If used on cdo griddes output captures first grid definition in full to use for regridding
    returns nothing'''
    f = open(file,"r")
    txt = f.read()
    newtxt = txt.split("#")[3] 
    new = open("gridfile.txt","w")
    new.write(newtxt)
    f.close()
    new.close()
    
    
def imerg_to_wrfout(imerg_path,wrfout_path,start,end): 
    ''' takes in  two paths for IMERG/WRFOUT as strings, and  start/end times as strings in format YYYY_MM_DD
    combines half-hourly IMERG '''
    imerg = glob.glob(f"{imerg_path}/*nc4.rg")
    wrfout = glob.glob(f"{wrfout_path}/*wrfout")
    assert len(imerg) > 0, "no regridded files found in imerg path
    assert len(wrfout) > 0, "no wrfout files found in wrfout path
    imerg_cube = imerg_to_cube(imerg)
    startdate = datetime.strptime(start,"&Y-%m-%d")
    enddate = datetime.strptime(end,"&Y-%m-%d")
    for file in wrfout:
        # big string manip to get seconds_since_1970 from filename. Will break if filename does not end in _YYYY-MM-DD_HHMMSS
        ftime = datetime.strptime("-".join(f[0].split("_")[-2:])[:-4],"%Y-%m-%d-%H") - datetime(1970, 1, 1)
        if startdate =< ftime =< enddate:
            # get index of imerg time that matches wrfout_time
            imerg_data = imerg_cube[imerg_cube.coord("time").nearest_neighbour_index(ftime.total_seconds())].data
            wrf_netcdf =  netCDF4.Dataset(file)
            wrf_netcdf.variables("RAINNC")[0,:,:] = imerg_data 
            wrf_netcdf.variables("RAINC")[:,:,:] = np.zeroslike(wrf_netcdf.variables("RAINC")[:,:,:]) # set RAINC to zero
            wrf_netcdf.close()
    
    
def imerg_to_cube(paths):
    ''' loads in and combines half-hourly IMERG data into a single cube of hourly data
    takes in a path as string, returns a cube of hourly imerg sums'''
    imerg_cube = iris.load(paths)
    iris.util.equalise_attributes(imerg_cube)
    imerg_cube.concatenate_cube()
    iris.coord_categorisation.add_hour(imerg_cube,"time")
    iris.coord_categorisation.iris.add_day_of_year(imerg_cube,"time") 
    imerg_cube.aggregated_by(["day_of_year","hour"],iris.analysis.SUM)
    return imerg_cube

    
if __name__ == "__main__":
    '''magic function, allows functions of file to be run from command line'''
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:]) # run function in arg1 with args 2+ as input