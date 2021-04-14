# AudioSet Download and Use In Meta-Learning
A convenient set of tools for downloading a quality controlled version of AudioSet in Python, with additional considerations for Meta-Learning based on current and on-going research.


Released by Google in 2017, the [AudioSet](https://research.google.com/audioset/) ontology consists of 632 hierarchically structured audio event classes spanning 2,084,320 10-second long samples. Other useful resources for understanding and using AudioSet:
- [Blog](https://ai.googleblog.com/2017/03/announcing-audioset-dataset-for-audio.html) post by Google at launch with some general details on the collection and labelling process.
- The TensorFlow research [branch](https://github.com/tensorflow/models/tree/master/research/audioset#models-for-audioset-a-large-scale-dataset-of-audio-events) for the set and its accompanying models.

<img src="images/AudioSet_logo.png" width="500" height="100" class="center"/>

Some important things to know about this dataset are the following:
- The raw data samples are not readily avilable for download(which is why this repo and others like it exist). Instead the data has been pre-feature-extracted using Google's own [VGG-ish network](https://github.com/tensorflow/models/tree/master/research/audioset/vggish), the output for whch is a 128-dimentional feature vector for every second of a given sample(1Hz).
- In the bulk of the meta data supplied with the set that enables us to scrape it from YouTube, the classes are not labelled by name of event, but instead by some id. Id -> class name conversions are/can be done using the 'ontology.json' file.
- Estimated qualities of sound events are given in the form of true counts per some number of samples form a given class. This additional level of evaluation appears to manual with a true count representeing the event appearing within a class sample, e.g if 8 out of 10 samples in some class contained the event it should it would have an 80% estimated quality.


## Basic Download Details
Should include here:
- How to set up the hyper params and main YAML file for teh scripts
- How the num samples works, i.e there raent an equal number per class, so you get up to num in class if n> num in class
- How teh different scripts thmselves interlink, creation of big data etc
- rough space needed on dirve etc/ sizes of files and clips


## Different Scripts
There are two different download scripts included in this repo, these include a single threaded version(also referred to as the normal one) primarily built around the idea of reproducibility and a multithreaded version that was built with the intention of trading off some reproducibility in favour of raw speed. In their current states, the recommendation is to **use the single threaded version**(single_thread_download.py). This is for a few reasons:
- The better reproducibility of the normal script allows for exact rebuilding of the set which can be invaluable in the case of data loss or corrution.
- The multiporceesing version, in its current implementtaion is not faster in most situations. This could be due to a few different isses, covered in a later [section](#markdown-Potenial Improvements). The code is also capable of saturating both CPU cores and network connection (tested on Ryzen 2700x and 100 Mbps connection) and so could cause significant slowdowns of the device/network being used.


## Reproducibility & Exceptions
INclude:
- How the scripts try to be reproducible. The successes and failures here
- potential issues with getting the exact same data gaain, ile videos being removed or privated etc - surprisingly common
- A large dataframe/ csv fle is generated which contains all amples downlaoded and put into the set

## Possible Issues
Is possible for YouTube to throttle access to their site after too many access requests. There are a few potential ways around this, these are:
- Setting some fixed time delay between downloads. This is very simple to set in the main control YAML file however comes with the caviat of significantly slowing down the full download process.
- Adding a cookies.txt file to the main script folder using your own YouTube and/or Google credentials. This is a bit more involved to set up however should allow the downoad to continue at normal speed. How to do this is covered in the Section  [Using A Cookies File](#markdown-Using-A-Cookies-File).
- 
- Youtube-dl updates etc(explain)

## Post Proccessing Notes
Include:
- How audio data should be scaled before spectrogram etc 
- additional file cleaniong, ie removing samples that arent correct langth

## Meta-Learning Considerations
Include:
- How current ppaers(two of them) deal with audioset and why thye do it in this way- ref
- what have we done to follow and what differences have been made
- Best recommendation for setting up this data for meta-learning based on all of these considerations

## Using A Cookies File

One of the methods of getting around YouTube's 'Too Many Requests' issue is to use a cookies file whihc contains your encoded personal Google Credentials for use in the YouTube-DL package. This can be done by following these steps:
- Add the following extension to a chromium based browser(i.e Edge, Chrome etc) [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg). This extension helps collect the cookie data from the websites that have been used.
- Open Google or Youtube in a new tab and sign into an account.
- In this same tab Click the EditThisCookie extension and navigate to the top bar. Click the export button (5th from the left in my current version), this will copy the cookies needed into the clipboard.
- Paste this data into a new .txt file and save it as 'cookies.txt'
- Place this file in the main script directory.
- Set the 'cookies' argument in the 'control.yaml' file to a 1. 
- Run either of the available download scripts as normal

## Potenial Improvements
Although the download codes included in this repo function as intended and were perfectly sufficient for obtaining the slice of AudioSet that was sought after, there is definitely still room for improvement. Im sure there are many people that will be able to suggest better tweaks but the folowing are ones that I think could make a fair amount of difference with respect to time optimisation and ease of use:



## References
Websites and Other Repositories:
- [AudioSet](https://research.google.com/audioset/index.html)
- [AudioSet GitHub](https://github.com/audioset/ontology)
- [Another Python based AudioSet download Repo which inspired this repos creation. Also contains links to learn more about Voice Computing](https://github.com/jim-schwoebel/download_audioset)

Research Papers:
- ["Audio Set: An ontology and human-labeled dataset for audio events"](https://research.google/pubs/pub45857/)
- ["Few-shot Acoustic Event Detection via Meta Learning"](https://arxiv.org/pdf/2002.09143.pdf)
- ["A Study of Few-Shot Audio Classification"](https://arxiv.org/abs/2012.01573)
