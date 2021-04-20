"""
When originally obtained the meta-data for unbalanced training set was unable 
    to be loaded by pandas due to header layering issues. The file at 100Mb was 
    too large ot be opened and edited by excel ina nice manner. This was worked 
    around by breaking up the csv into three parts and fixing them individually.
    As editing the csv meta files before import into some software may be
    useful, the unbalanced set is kept split up in this repo.

This script deal with the reocmbination and reformatting of all meta-data files.
    These include:
        - balanced_train_segments
        - eval_segments
        - unbalanced_train_segemnts_0
        - unbalanced_train_segemnts_1
        - unbalanced_train_segemnts_2

The file should only ever have to be run once after the repo has been downloaded

As this general data download approach is to be used for meta-learning, the eval
    segments file is also compiled along with the rest since evalutaion for
    type of meta-learning being investigated occurs more class wide than data wide.

REQUIRES:
    - All examples meta data csv files, hosted in MetaData folder

OUTPUTS:
    - big_data.csv, a csv file located in the MetaData folder which contains all
        examples of classes from available meta-data
"""

###############################################################################
#IMPORTS AND DIRECTORY POINTING
###############################################################################
import os
import warnings
import numpy as np
import pandas as pd

warnings.simplefilter(action='ignore', category=FutureWarning)


###############################################################################
# BIG DATAFRAME CREATION
###############################################################################
def compile_dataframes(path_to_meta):
    """
    Function creates a large compiled dataframe of all available meta-data in 
        the meta-data folder passed

    :param path_to_meta: str
        The directory path to the meta data folder

    :saves: csv file
        A file with all available meta-data compiled into one
    """
    # Meta data sheet imports
    eval_segments = pd.read_csv(path_to_meta + '\\eval_segments.csv', header=[1], low_memory=False)
    balanced_train = pd.read_csv(path_to_meta + '\\balanced_train_segments.csv', header=[1], low_memory=False)
    unbalanced_train_0 = pd.read_csv(path_to_meta + '\\unbalanced_train_segments_0.csv', header=[1], low_memory=False)
    unbalanced_train_1 = pd.read_csv(path_to_meta + '\\unbalanced_train_segments_1.csv', header=[1], low_memory=False)
    unbalanced_train_2 = pd.read_csv(path_to_meta + '\\unbalanced_train_segments_2.csv', header=[1], low_memory=False)

    # Concatenates all the imported dataframes into one much larger one, ~2M samples
    big_data = pd.concat([balanced_train, unbalanced_train_0, unbalanced_train_1,
                          unbalanced_train_2, eval_segments], axis=0, ignore_index=True)

    # The labels (all columns after the third) need to be cleaned of quotation marks
    big_data_first_three = big_data.iloc[:, 0:3] # Takes the columns to preserve
    big_data_rest = big_data.iloc[:, 3:] # Takes columns of labels to clean

    # Applies a string cleaning operation to all of the label columns
    big_data_rest_cleaned = big_data_rest.apply(lambda x: x.str.strip(' "'), axis=1)

    # Concats the two split dataframes back together before finally saving
    big_data_full_cleaned = pd.concat([big_data_first_three, big_data_rest_cleaned], axis=1, ignore_index=True)
    big_data_full_cleaned.to_csv(path_to_meta + '\\big_data.csv')