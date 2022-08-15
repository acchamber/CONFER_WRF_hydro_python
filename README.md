# CONFER_WRF_hydro_python
A Repository for various tools and examples using python and the iris library with WRF-hydro outputs and inputs. 

Currently consists of: 

**WRF_output_plotting.ipynb **

example of loading and plotting coupled WRF-hydro outputs in Iris. Examples in the notebook were done with one of Joel's monthly output files - wrfout_d02_2011-04-01_00:00:0 - which is not included in repo due to being 7.4 GB 

**WRF_precip_replacement.sh
WRF_precip.py**

A shell script and python file that have been developed to replace an existing matlap script to force the rainfall in a wrfout file from uncoupled WRF with IMERG rainfall data instead. Shell script is designed to be run from the command line, futher instructions in the .sh file itself (along with comments in the .py) 
