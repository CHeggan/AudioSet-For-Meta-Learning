"""
This script parses through all classes available in Google's AudioSet dataset
    collection. Using the available meta data for the set such as quality estimated
    for each class and whether or not they have child classes, designated
    'suitable_classes' are found and saved for later use in downloading and sorting.

REQUIRES:
    - 'MetaData' folder that holds the following files(Should contain others for later):
            - labels.xlsx :        mID to name conversion table for classes
            - ontology.json :      AudioSet ontology which includes all meta dta about classes
            - qa_true_counts.csv : Estimated quality of classes from Google's testing

OUTPUTS:
    - A numpy loadable file which contains a 2D array with the classes from
        AudioSet that meet requirements, the first dimension is the mID and
        second dimension is the readable name of class
    - option for a PNG plot of how number of available classes scale with quality threshold
        - Just uncomment graphing() call in main 
    - Printed number of classes found
"""

###############################################################################
#IMPORTS
###############################################################################

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


###############################################################################
#FUNCTIONS
###############################################################################
def suitable_class_extractor(quality, path_to_meta, leaf=True):
    """
    Function to extract suitable classes from the AudioSet ontology based on 
        some requirements

    :param qual: float 
        Minimum quality threshold for considered classes, between 0 and 1
    :param leafs: Boolean 
        Whether or not to only consider leaf nodes of AudioSet hierarchy

    :return len(suitabe): int
        Number of suitable classes found from ontology
    :return suitable: array
        2D array with mIDs along with legible class names (suitable_classes.npy)
    """

    # Read in mid to label conversion table
    label_convert = pd.read_excel(path_to_meta + '\labels.xlsx', index_col=0)

    # Read in ontology stored in json file
    with open(path_to_meta + '/ontology.json') as f:
        ontology = json.load(f)

    # Read in quality estimates for classes
    quality_estimates = pd.read_csv(path_to_meta + '/qa_true_counts.csv')
    quality_estimates['rate'] = quality_estimates['num_true'] / quality_estimates['num_rated']

    # Stores the suitable classes to extract in 2D, [mid, label_name]
    suitable = []
    for i, val in enumerate(ontology):
        example = ontology[i]

        # Checks if leaf node or not
        if leaf:
            if len(example['child_ids']) > 0:
                continue

        if example['restrictions'] == ['blacklist']:
            continue

        mid = example['id']
        sub_df = quality_estimates.loc[quality_estimates['label_id'] == mid]

        # Some classes do not seem to exist outside of the ontology and so skip
        if sub_df.empty:
            continue

        # Make sure that quality threshold is reached
        if (sub_df['rate'].item() >= quality):
            sub_label = label_convert.loc[label_convert['mid'] == mid]
            mid_name = sub_label['display_name'].item()
            # If both requirements satisfied we save class by name and MID
            suitable.append([mid, mid_name])

    return len(suitable), suitable


def graphing(path_to_meta):
    """
    Determines number of available classes(leaf nodes) that are available
        at various quality thresholds

    :save: PNG 
        Graph of how number of suitbale classes scale with estimated
            quality threshold
    """
    # Deals with data collection
    numbers_of_classes = []
    thresholds = np.arange(0, 1.05, 0.05)
    for i in thresholds:
        nums, classes = suitable_class_extractor(i, path_to_meta, True)
        numbers_of_classes.append(nums)

    # Takes data and plots/saves
    plt.figure(figsize=(15, 10))
    plt.plot(thresholds, numbers_of_classes)
    plt.xlabel('Quality Threshold')
    plt.ylabel('Number of Leaf Classes Available')
    plt.savefig('audioset_leafs_per_threshold_quality.png')
    plt.show()


###############################################################################
# MAIN FUNCTION WITH CALL
###############################################################################
def main_get_classes(leafs, qual, path_to_meta):
    """
    Main file function which calls everything required

    :param qual: float 
        Minimum quality threshold for considered classes, between 0 and 1
    :param leafs: Boolean 
        Whether or not to only consider leaf nodes of AudioSet hierarchy

    :print: int
        Number of suitable classes found from ontology
    :save: array
        2D array with mIDs along with legible class names (suitable_classes.npy)
    """
    if leafs == 'n':
        num_classes, classes = suitable_class_extractor(qual, path_to_meta, False)
        print(f'{num_classes} suitable classes found in AudioSet using passed parameters')
    else:
        num_classes, classes = suitable_class_extractor(qual, path_to_meta, True)
        print(f'{num_classes} suitable classes found in AudioSet using passed parameters')

    # Saves the 2D class array to a npy file for later loading
    np.save('suitable_classes', classes)
    #graphing(path_to_meta)
