# AudioSet Download and Use In Meta-Learning    [![CodeFactor](https://www.codefactor.io/repository/github/cheggan/audioset-for-meta-learning/badge?s=750292eb018de440a569bba7ac43889da24f176e)](https://www.codefactor.io/repository/github/cheggan/audioset-for-meta-learning)
A convenient set of tools for downloading a quality controlled version of AudioSet in Python, with additional considerations for Meta-Learning based on current and on-going research.


Released by Google in 2017, the [AudioSet](https://research.google.com/audioset/) ontology consists of 632 hierarchically structured audio event classes spanning 2,084,320 10-second long samples. Other useful resources for understanding and using AudioSet:
- [Blog](https://ai.googleblog.com/2017/03/announcing-audioset-dataset-for-audio.html) post by Google at launch with some general details on the collection and labelling process
- The TensorFlow research [branch](https://github.com/tensorflow/models/tree/master/research/audioset#models-for-audioset-a-large-scale-dataset-of-audio-events) for the set and its accompanying models

<img src="images/AudioSet_logo.png" width="500" height="100" class="center"/>

Some important things to know about this dataset are the following:
- The raw data samples are not readily available for download(which is why this repo and others like it exist). Instead the data has been pre-feature-extracted using Google's own [VGG-ish network](https://github.com/tensorflow/models/tree/master/research/audioset/vggish), the output for which is a 128-dimensional feature vector for every second of a given sample(1Hz)
- In the bulk of the meta data supplied with the set that enables us to scrape it from YouTube, the classes are not labelled by name of event, but instead by some id. Id -> class name conversions are/can be done using the 'ontology.json' file
- Estimated qualities of sound events are given in the form of true counts per some number of samples form a given class. This additional level of evaluation appears to manual with a true count representing the event appearing within a class sample, e.g if 8 out of 10 samples in some class contained the event it should it would have an 80% estimated quality

## Citation
This code-base was written to support our investigation of few-shot acoustic classification. If you use any of the code included here, please cite our work which we used it for:
```
@article{MetaAudio,
  author = {Calum Heggan et al.},
  title = {Meta-Audio: A Few-Shot Audio Classification Benchmark},
  year = {2022},
  publisher = {ICANN},
}
```

## Enviroment
We use miniconda for our environment setup. For the purposes of reproduction we include the environment file. This can be set up using the following command:
```
conda env create --file youtube_download_env.txt
```

## Basic Download Details
### Scripts & Programs
Prior: You need to have the ffmpep.exe executable file located within the main directory of the code base

The codes are written in such a way that only a few files ever have to be accessed or explicitly ran by a user. These include:
 - control.yaml (Contains all of the parameters needed to run the codes included)
 - get_relevant_meta_data.py (Generates suitable classes based on parameters in control file and compiles relevant metadata together)
 - download_data.py (The main download function, this will be the script that will need to be left running/restarted where necessary)

### How To Run
Starting off, it is important to look at the control file listed above and tune the parameters needed for downloading the data, e.g. leaf nodes, minimum estimated quality and number of unique samples to try and download per suitable class. On top of this it is important to note that that we can also set a start and end index here which work over all of our 'suitable classes'. This allows us to download class-wise slices of our full dataset of interest at a time, meaning that the main code does'nt have to be left running and then arbitrarily killed off. 

Next we have to generate the list of classes we want to download data from as well as compile all of our relevant meta-data together. We do this by running the following:
```bash
python get_relevant_meta_data.py
```

The last step is to go ahead and run the main download function. If using teh control file to split over teh classes of interest, just remember that you will have to run the download function for all of the classes, indexing both the start and the end up in the control file as you do i.e. old end becomes new start and so on.

```bash
python single.py
```

## Reproducibility & Exceptions
The datasets that the download scripts generate aim to be exactly reproducible excluding some exceptions that may occur. The scripts achieve this by:
- Packages seeding for both the random sampling of the class specific sub-dataset which is used to grab Youtube Video-IDs(YIDs) to download and for the splitting of the full set into meta-sets
- A csv file/dataframe of downloaded files is generated for each class and is contained within the same folder as the class data itself. This file has the YIDs of all downloaded files along, the class id/proper name and the YID->filename conversions for each data sample
- A full dataset dataframe containing the needed meta-data to reconstruct the full set without any of the first steps again. This is paired with a script that can rebuild the full set once again from this one dataframe(once again be cautious of exceptions and now unavailable files). This reconstruction would then contain no files that weren't in the first one along with the added benefit of downloading more quickly as much of the overhead has already been done

The potential exceptions that may prevent exact datasets being reproduced from scratch are all due to the availability of specific samples from Youtube, these include:
- Video deletion, removal or privatisation
- Geographical restricted access
- Required to sign in(this specific issue can be mitigated with cookies file addition)
- User account deletion

## Possible Issues
It is possible for YouTube to throttle access to their site after too many access requests. There are a few potential ways around this, these are:
- Setting some fixed time delay between downloads. This would be very simple to implement in the main control YAML file however would come with the caveat of significantly slowing down the full download process
- Adding a cookies.txt file to the main script folder using your own YouTube and/or Google credentials. This is a bit more involved to set up however should allow the download to continue at normal speed. How to do this is covered in the Section  [Using A Cookies File](#markdown-Using-A-Cookies-File)
- Youtube-dl being out of date (Most of the time simply updating this makes things work smoothly again but sometimes, other environment clashes occur which have to be fixed)

## Post Proccessing Scripts
Included within our other adjacent [repository](https://github.com/CHeggan/MetaAudio-A-Few-Shot-Audio-Classification-Benchmark) is a variety of post-processing scripts, specifically designed for parsing over the full dataset in one sweep. There is also a few other helpful codes included here focused around using datasets like this one for meta-learning and machine-learning in general. Some example scripts include:
- Dataset cleaning which removes invalid samples, i.e silence for the full audio clip
- wav to numpy (.npy) file conversion. This speeds up raw data loading into python by about 80x and reduces the total storage size by about 2x as well
- Raw audio to spectrogram conversion
- PyTorch dataset classes
- Global and channel spectrogram normalisation

## Using A Cookies File
One of the methods of getting around YouTube's 'Too Many Requests' issue is to use a cookies file which contains your encoded personal Google Credentials for use in the YouTube-DL package. This can be done by following these steps:
- Add the following extension to a chromium based browser(i.e Edge, Chrome etc) [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg). This extension helps collect the cookie data from the websites that have been used.
- Open Google or Youtube in a new tab and sign into an account.
- In this same tab Click the EditThisCookie extension and navigate to the top bar. Click the export button (5th from the left in my current version), this will copy the cookies needed into the clipboard.
- Paste this data into a new .txt file and save it as 'cookies.txt', it doesn't necessarily matter where
- Get the exact path to the cookies file
- Set the 'cookies' path in 'control.yaml' as the path you just got 
- Run either of the available download scripts as normal

## Potential Improvements
Although the download codes included in this repo function as intended and were perfectly sufficient for obtaining the slice of AudioSet that was sought after, there is definitely still room for improvement. Im sure there are many people that will be able to suggest better tweaks but the there are still some included here as a rough show of how things could be improved.

General:
- On passes of the script and the main meta-data sets, files that are unavailable due to any of the possible exemptions listed earlier or corrupted could be tracked and their details stored in another file or erased from the main meta-data file. Both of these could be used in order to reduce total script execution time on recreations of sets, or creation of new and overlapping ones.


Multiprocessing:
- One of the main things that appear to be slowing down our trial multiprocessing script is some large gap between downloading all files within a class and then converting them using ffmepg. Inferring form local runs, this effect approximately doubles the time of the script. It is not clear what exactly is causing this gap as the overheads for multi is reported by python at less than 1%. Reformatting the current version into two scripts(a download and a reformating/cleaning) could be an interesting way of getting around this and obtaining the expected speedup.
- As noted earlier, the generated dataframe containing YIDs of downloaded samples is not exact for this version and instead contains all files that has their downloads attempted. Finding some solution around this would put it further in line with the reproducibility capability of teh single threaded version.


## References
Websites and Other Repositories:
- [AudioSet](https://research.google.com/audioset/index.html)
- [AudioSet GitHub](https://github.com/audioset/ontology)
- [Another Python based AudioSet download Repo which inspired this repos creation. Also contains links to learn more about Voice Computing](https://github.com/jim-schwoebel/download_audioset)

Research Papers:
- ["Audio Set: An ontology and human-labeled dataset for audio events"](https://research.google/pubs/pub45857/)
- ["Few-shot Acoustic Event Detection via Meta Learning"](https://arxiv.org/pdf/2002.09143.pdf)
- ["A Study of Few-Shot Audio Classification"](https://arxiv.org/abs/2012.01573)
