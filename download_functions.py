"""
This script takes some csv file with all example meta data including
    YIDs and downloads the wanted files/ classes within. The data is downloaded
    into seperate folders with included logs of what YID the raw data was taken
    from before being snipped into 10s clips and converted to .wav. This log is
    included/ created for reproducibility reasons, as using only these, each class
    worth of samples can be easily recreated exactly if needed, minus exceptons.

Using some additional fine tuning within the file_cleaning function could easily
    allow for shorter clips to be taken than Google's stated 10s.

The quanity of examples per class varies drastically where some are as low as
~100 and as high as ~20,000.

The whole srcipt, if done for many classes at once(slices in main function call)
    takes a fairly large quanity of time due to the approach taken here,
    which to some extent trades off CPU efficiency for additional reproducibiltiy
    control as well as allowing the code to run in a stop start function(more
    details in .md file).

REQUIRES:
    - Some compiled meta-data csv file located within MetaData folder
    - Sufficient disk space (~40Gb for 200 10s .wav files in each of 142 classes),
        ~ 1-2 Mb per 10s clip - scale accordingly

OUTPUTS:
    - Folder 'AudioSet_data' with all class folders located inside, each with n
        downloaded and snipped samples
"""

###############################################################################
#IMPORTS AND DIRECTORY POINTING
###############################################################################
import os
import io
import ffmpy
import ffmpeg
import warnings
import youtube_dl
import numpy as np
import pandas as pd
import soundfile as sf

from tqdm import tqdm, trange

from contextlib import redirect_stdout, redirect_stderr

warnings.simplefilter(action='ignore', category=FutureWarning)


###############################################################################
#DATA IMPORTS
###############################################################################
def get_data(path_to_meta, df_file):
    """
    Function loads all of teh required meta-data from files in directory

    :param path_to_meta: str
        Path to teh meta-data form the current working directory

    :return labels: array
        An array of the suitable unique class Ids
    :return textabels: array
        Te human readbale equivalents to variable 'labels'
    :return big_data: dataframe
        All meta-data containing dataframe from which we sample relevant subsets
    """
    # Deals with the import of big_data.csv, created in compile_data.py
    big_data = pd.read_csv(path_to_meta + '\\' + 'big_data.csv', index_col=0)
    # YouTube ID(col1) has to be changed so we can do a comparison on columns later on
    big_data = big_data.rename(columns={"0": "YID"})

    # Imports the perviosuly used suitable_classes.npy file array
    suitable_classes = np.load('suitable_classes.npy')
    labels = suitable_classes[:,0]
    textlabels = suitable_classes[:,1]

    return labels, textlabels, big_data

###############################################################################
#FUNCTIONS
###############################################################################
def download_audio(link, start, end, cookie_path):
    """
    Function responsible for actually downloading the file from youtube. This
        is mainly done through the youtube_dl library where options are used
        to only grab the audio.

    :param link: str
        The youtube compatible link for the file attempting to
            be downloaded

    :return filename: str
        The name of the file, a return of '0' indicates a
            download failure, anything else should be a success.
    """
    # Names the file straight away, if not changed by return, failure has occured
    filename='0'
    # Obtains a list of files in directory, important for later identifying download
    listdir=os.listdir()

    # Options for the downloading of file, in this case we want bets quality audio
    options = {
    'quiet': True, # Mutes normal output
    'no-warnings': True, #Mutes warnings
    'ignore-errors': True, # Ignores errors, i.e exceptions etc
    'format': 'bestaudio/best', # Downloads the best quality audio
    'extractaudio' : True,  # only keep the audio
    'noplaylist' : True,    # only download single song, not playlist
    }

    # if we have a cookie path we can use it
    if cookie_path != 'None':
        options['cookiefile'] = cookie_path # Path to the cookies file


    # The code here uses try to avoid a crash when rare downloads inevitably fail
    try:
        f = io.StringIO()
        with redirect_stdout(f), redirect_stderr(f):
            youtube_dl.YoutubeDL(options).download([link])

        # Comapres new to old directory file lists to find the new file
        listdir2=os.listdir()
        for i, val in enumerate(listdir2):
            if listdir2[i] not in listdir:
                filename=listdir2[i]
                break

        # want to check teh length of the file so that we dont have smaples< 10s
        length = youtube_dl.YoutubeDL(options).extract_info(link)['duration']

        # Files that are excatly 10s typically get shortened by a second, so 11s needed
        if  length < 11:
            os.remove(filename)
            filename='0'
        # Wierd start/ends have been selected for some files so have to sort this
        if end >= length:
            os.remove(filename)
            filename='0'

        if end-start != 10:
            os.remove(filename)
            filename ='0'


    # Skips forward if try function fails, indicating the fle cannot be retrieved
    except Exception:
        filename ='0'

    return filename


def create_directories(textlabels, expected_dir):
    """
    Function responsible for creating the dataset directory along with each
        individual class folder.

    :param textlabels: array
        The readable class labels for folder creation
    :param expected_dir: str
        The parent dataset directory, this variable is needed
            for a check used to prevent nesting that can otherwise occur.

    :save: directories
        Creates the main 'AudioSet_Data' folder along with class specific folders
    """
    try: # Tries to find audiodataset folder and set as current directory
        defaultdir2=os.getcwd()+'/AudioSet_Data/'
        os.chdir(os.getcwd()+'/AudioSet_Data')
    except Exception: # If cant find one, makes new and sets as CWD
        # This conditional stops the code from nesting infinitely
        if os.getcwd() == expected_dir:
            pass
        else:
            defaultdir2=os.getcwd()+'/AudioSet_Data/'
            os.mkdir(os.getcwd()+'/AudioSet_Data')
            os.chdir(os.getcwd()+'/AudioSet_Data')

    # Creates a unique folder for every class based on textlabels if doesnt exist already
    for i, text_label in enumerate(textlabels):
        try:
            os.mkdir(text_label)
        except Exception:
            created = False
            continue


def file_cleaning(filename, num_sample, start, end, defaultdir):
    """
    This function cleans/clips teh downloaded audio clip to the specific 10s range
        that describes the clas in question. Also converts the file to .wav and
        renames it so the class datasets are more cohesive in naming convention.

    :param filename: str
        The current name of the file as given by download function
    :param num_sample: int 
        Identifying number of the file within class, i.e if
            num_sample = 5, this is the 5th file downloaded in this class
    :param start: int 
        Start time in seconds of the class clip form raw file
    :param end: int 
        End time in seconds of the class clip form raw file
    :param defaultdir: str 
        The base directory of the full codeset, i.e '...\AudioSet',
            this is needed to point to the ffmpeg.exe file used for conversion


    :return filename: str 
        The new name of the file with the numbering convention
    :return samplerate: int
        The samplerate determined by soundfile library, is returned
            so that it can be noted in saved example data

    :save: .wav file
        Saves the recently downloaded file under a new name after clipping to
            the 10s example
    """
    # Grabs the extension from the file name
    extension = os.path.splitext(filename)[1]

    # Renames the file with num of sample/ start and end times
    os.rename(filename,'%s%s'%(num_sample,extension))

    # Redefines new filenames
    filename='%s%s'%(num_sample,extension)

    # If the file type isnt already .wav, we want to change it to be
    if extension not in ['.wav']:
        xindex = filename.find(extension)
        filename = filename[0 : xindex]

        # Uses the executable ffmpeg file to run audio conversion, needs default directory
        ff = ffmpy.FFmpeg(executable = defaultdir + '\\ffmpeg.exe',
            global_options = ('-hide_banner -loglevel panic -nostats'),
            inputs = {filename + extension:None},
            outputs = {filename +'.wav':None},
            )
        ff.run()
        os.remove(filename+extension)

    # Uses information of the audio sample to cut it down to the 10s interval specified in metadata
    file = filename+'.wav'
    data, samplerate = sf.read(file)
    totalframes = len(data)
    totalseconds = totalframes / samplerate
    startsec = start
    startframe = samplerate * startsec
    endsec = end
    endframe = samplerate * endsec

    # Writes the newly cut down file
    os.remove(file)
    sf.write(file, data[int(startframe):int(endframe)], samplerate)

    return file, samplerate

###############################################################################
#MAIN FUNCTION
###############################################################################
def main_download(defaultdir, samples_per_class, labels, textlabels, big_data, cookie_path, seed):
    """
    Function that brings all things together to download all class datasets.

    :param samples_per_class: int
        How many samples to attempt to download per class
            label given
    :param labels: array
         Class labels to be downloaded, this list is the MIDs
    :param textlabels: array
        Readable class labels to be downloaded, should
            line up with MIDs from labels list
    :param big_data: Dataframe 
        Includes all examples spanning all classes
    : param cookie_path: str
        Absolute path to the cookies file being used for downloading
    :param seed: int
        Random sampling seed for reproducibility

    :save: Downloads, cleans and snips audio samples for each class given, up to
        limit of num_samples or until examples of class run out
    """
    # Need to some expected directory to stop nesting, has to have the \\
    expected_dir = defaultdir + '\\AudioSet_Data'

    # Creates all needed directories if they dont already exist
    create_directories(textlabels, expected_dir)

    # Start of every link that will be needed
    slink='https://www.youtube.com/watch?v='

    for i in trange(len(labels)):
        # Access sub dataset folder
        os.chdir(os.getcwd() + '\\' + textlabels[i])

        all_examples = big_data[big_data.eq(labels[i]).any(1)]
        available = all_examples.shape[0]

        files_downloaded, num_failed = 0, 0

        try: # Tries to find log of files that have been downloaded
            class_df = pd.read_csv(textlabels[i] + '.csv')
            # Finds how mnay files done so far for class and accounts for them in running total
            num_files = class_df.shape[0]
            files_downloaded += num_files
            # Combining the dataframes and then removing duplicated based on first column
            all_examples = pd.concat([all_examples, class_df]).drop_duplicates(subset='YID', keep=False,
                                                                               inplace=False, ignore_index=False)
        except Exception:
            class_df = pd.DataFrame(columns=['YID','MID','CLASS NAME','FILE NAME',
                        'OG FILE', 'SR'])

        # Sets how many files we actually want to/ can extract before accounting for
        to_get = min(samples_per_class, available)

        if files_downloaded >= to_get:
            os.chdir(expected_dir)
            #print('Skipping: {}'.format(labels[i]))
            continue

        while True:
            # Randomly samples the all_examples df without replacement
            instance = all_examples.sample(1, random_state=seed)
            all_examples = all_examples.drop(instance.index)

            # If no more yids to sample
            if all_examples.empty:
                print(f'{files_downloaded} files downloaded for class {labels[i]}')
                # Need to return to parent directory
                os.chdir(expected_dir)
                break

            # Creates the youtube link used for actually downloading
            yid = instance.iloc[0, 0]
            link = slink + yid

            # Additional meta data retrival
            start = instance.iloc[0, 1]
            end = instance.iloc[0, 2]

            # Attempts the file download, fails return '0'
            filename = download_audio(link, start, end, cookie_path)

            # If file fails we move onto next sample
            if filename == '0':
                num_failed += 1
                print('failed')
                continue

            # Track the successful download
            files_downloaded += 1

            # Cleans the file, incuding snipping, and returns the new file name, {num}.wav
            new_filename, sr = file_cleaning(filename, files_downloaded, start, end, defaultdir)

            # Save new collected files to relevent dataframe and save the dataframe
            class_df = class_df.append({'YID': yid, 'MID': labels[i], 'CLASS NAME': textlabels[i],
                                        'FILE NAME': new_filename, 'OG FILE':filename, 'SR':sr}, ignore_index = True)
            class_df.to_csv(textlabels[i] + '.csv')

            # Finishing conditions for downloads
            # If no more yids to sample
            if all_examples.empty:
                print(f'{files_downloaded} files downloaded for class {labels[i]}')
                # Need to return to parent directory
                os.chdir(expected_dir)
                break

            #If we have the correct number of samples that we need
            elif files_downloaded >= to_get:
                os.chdir(expected_dir)
                break
