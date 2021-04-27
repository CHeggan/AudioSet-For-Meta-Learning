"""
Script deals with per-sample normalisation of the raw audio signals after they
    have been converted from wav to npy.
The main function iterates over the so called 'old_dir'and creates  a mirror
    directory in 'new_dir'.
The script assumes that the 'new_dir' directory has already been created.
"""
###############################################################################
# IMPORTS
###############################################################################
import numpy as np
import librosa
import yaml
import time
import sys
import os

###############################################################################
# DIRECTORIES
###############################################################################
old_dir = 'C:/Users/user/Documents/Datasets/AudioSet_meta_split_raw_array'
new_dir = 'C:/Users/user/Documents/Datasets/AudioSet_meta_split_raw_array_norm'

###############################################################################
# CONVERSION FUNCTION
###############################################################################
def file_conversion(new_dir, current_path):
    """
    Function loads a path of a specific data example and performs sample-wise
        normalisation, that is; The sample ends up with a mean of ~0 and a std
        ~ 1. This function assumes the current data samples are saved as .npy
        files.

    :param new_dir: str
        The path in which the new data sample should be saved
    :param current_path: str
        The current path of teh data sample looking to be loaded and normalised

    :save data: array
        The newly per-sample normalised data is saved to the new directory
    """
    # Loads the current data sample being looked at
    data = np.load(current_path)

    # If any samples have unreasonable stats, we dont bother saving and discard
    #   by simply returning without saving
    if np.std(data) == 0.0:
        print(f'File: {current_path} was not saved due to std=0')
        return
    if data.shape[0] != 160000:
        print(f'File: {current_path} was not saved due to length {data.shape[0]} != 160,000')
        return

    # Performs per-sample normaisation to mean 0 and std 1
    new_data = ((data - np.mean(data)) / np.std(data))

    file_name = current_path.split('\\')[-1]
    new_path = os.path.join(new_dir, file_name)
    #print(new_path, np.mean(new_data), np.std(new_data))

    # Saves the newly normalised sample to new directory
    np.save(new_path, data)

###############################################################################
# MAIN FUNCTION
###############################################################################
def main(old_dir, new_dir):
    """
    Iterates thorugh the folder structure of old directory and mirrors it in the
        new dir folder with per-sample normalised data.

    :param old_dir: str
        The base directory which we wish to mirror. Contains our current raw and
            un-normalised data
    :param new_dir: str

    """
    #sets working dir as array parent folder
    os.chdir(new_dir)

    splits = os.listdir(old_dir)
    for split in splits:
        print('\n')
        print(split)

        temp = os.path.join(old_dir, split)
        temp_new = os.path.join(new_dir, split)

        try:
            os.mkdir(temp_new)
        except:
            print(f'Already Created: {temp_new}')

        contained_classes = os.listdir(temp)

        for seen_class in contained_classes:
            working_dir = os.path.join(temp, seen_class)
            new_working_dir = os.path.join(temp_new, seen_class)

            try:
                os.mkdir(new_working_dir)
            except:
                print(f'Already Created: {new_working_dir}')

            for file in os.listdir(working_dir):
                if file.endswith('.npy'):
                    file_path = os.path.join(working_dir, file)

                    file_conversion(new_working_dir, file_path)



main(old_dir, new_dir)
