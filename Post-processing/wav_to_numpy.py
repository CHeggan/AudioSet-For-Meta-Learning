"""
Script deals with dataset wide conversion from .wav files to .npy files. The
    main motivation behind this is that .npy files can be loaded significantly
    faster into python than .wav files(~80x). This also allows other conversions,
    like the one to spectrograms, to be done much more quickly.
"""

###############################################################################
# IMPORTS
###############################################################################
import numpy as np
import librosa
import time
import os

###############################################################################
# DIRECTORIES
###############################################################################
old_dir = 'X:/Datasets/AudioSet/AudioSet_meta_split_raw_wav'
new_dir = 'X:/Datasets/AudioSet/AudioSet_meta_split_raw_array'

###############################################################################
# CONVERSION FUNCTION
###############################################################################
def file_conversion(new_dir, current_path, sr):
    data, sr = librosa.load(current_path, sr=sr, mono=True)

    file_name = current_path.split('\\')[-1]
    new_path = os.path.join(new_dir, file_name)
    print(new_path)

    np.save(new_path, data)

###############################################################################
# MAIN FUNCTION
###############################################################################
def main(old_dir, new_dir):
    #sets working dir as array parent folder
    os.chdir(new_dir)

    splits = os.listdir(old_dir)
    for split in splits:
        print(split)
        print('\n')
        if split == 'Other':
            continue

        else:
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
                    if file.endswith('.wav'):
                        file_path = os.path.join(working_dir, file)

                        file_conversion(new_working_dir, file_path, 16000)



main(old_dir, new_dir)


"""
lib_start = time.time()
data, sr = librosa.load('X:/Datasets/AudioSet/AudioSet_meta_split_raw_wav/meta_train_raw/Acoustic guitar/1.wav', sr=16000, mono=True)
lib_end = time.time()
print('Lib load', lib_end-lib_start)

np.save('example_data.npy', data)

np_start = time.time()
data = np.load('example_data.npy')
np_end = time.time()
print('np time', np_end-np_start)
print(data.shape)


path = 'X:/Datasets/AudioSet/AudioSet_meta_split_raw_wav/meta_train_raw/Acoustic guitar/1.wav'
print(path.split('/')[-1])
"""
