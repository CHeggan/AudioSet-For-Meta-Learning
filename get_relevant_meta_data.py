"""
Main file for obtaining the meta data needed for downloading classes of interest. 
    Imports relevent parts from the other scripts and combines them all 
    in the expected order of execution.

The outputs of this file are the following:
    -> 'big_data.csv': a dataframe which contains meta data for all classes 
        contained in the selection made
    -> 'suitable_classes.npy': a numpy save file containing the selected class 
        IDs along with their human named counterparts
"""

##############################################################################
#IMPORTS
##############################################################################
import os
import yaml

from pathlib import Path
from get_classes import main_get_classes, suitable_class_extractor, graphing
from compile_data import compile_dataframes

##############################################################################
#MAIN
##############################################################################

if __name__== '__main__':

    # Open the 'control.yaml' parameter file and loads the options selected
    with open("control.yaml") as stream:
        params = yaml.safe_load(stream)


    # Sets the directory of the meta-data
    defaultdir=os.getcwd()
    path_to_meta = os.path.join(defaultdir, params['dir']['meta_folder'])


    # Looks for the 'big_data.csv' file -if not already made, will be created
    main_df = os.path.join(path_to_meta,'big_data.csv')
    main_df = Path(main_df)

    if main_df.is_file():
        pass
    else:
        print('Compiling meta-data files ..... This takes a fair few minutes, time for a coffee?')
        compile_dataframes(path_to_meta)
        print("The large joint dataframe 'big_data.csv' has been created")


    # This fucntion is contained within 'get_classes.py'
    # It generates a suitable class ID/name array whic is used to compile meta-data 
    main_get_classes(leafs=params['classes']['leafs'], 
                        qual=params['classes']['quality_threshold'],
                        path_to_meta=path_to_meta)


    print("If this in unsuitable, this file can be run again with changed params from 'control.yaml'")
