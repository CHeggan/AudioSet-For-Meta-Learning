"""
This file deals with starting the single threaded download process, which as of 
  right now is the recommended version to use(will update if this changes).
"""

##############################################################################
# IMPORTS
##############################################################################
import os
import yaml

from download_functions import get_data, main_download
from download_functions import download_audio, create_directories, file_cleaning

##############################################################################
# MAIN 
##############################################################################
if __name__ == '__main__':

    # Open the 'control.yaml' parameter file and loads the options selected
    with open("control.yaml") as stream:
        params = yaml.safe_load(stream)

    # Sets the directory of the meta-data
    defaultdir=os.getcwd()
    path_to_meta = os.path.join(defaultdir, params['dir']['meta_folder'])

    # Gets the meta data needed for the downloading run
    labels, textlabels, big_data = get_data(path_to_meta, params['dir']['df_file'])

    # Sets up a full run of the suitable set
    if params['data']['end_index'] == 'None':
        end_index = len(labels)
    # We have some numeric end point for this run, good for downloading in slices
    else:
        end_index = params['data']['end_index']

    # We also grab the start index. Can stay at 0 at all times in theory but 
    #   we keep option for greater user control, missing classes etc
    start_index = params['data']['start_index']


    # Starts the main download function
    main_download(defaultdir=defaultdir, 
                    samples_per_class=params['data']['max_per_class'],
                    labels=labels[start_index:end_index],
                    textlabels=textlabels[start_index:end_index],
                    big_data=big_data,
                    cookie_path=params['dir']['cookie_path'],
                    seed=params['seed'])