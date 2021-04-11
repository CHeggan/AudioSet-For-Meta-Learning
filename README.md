# AudioSet Download and Use In Meta-Learning
A convenient set of tools for downloading a quality controlled version of AudioSet in Python, with additional considerations for Meta-Learning based on current research.


Released by Google in 2017, the [AudioSet](https://research.google.com/audioset/) ontology consists of 632 hierarchically structured audio event classes spanning 2,084,320 10-second long samples. Some importtant things to know about this dataset are the following:
- The raw data samples are not readily avilable for download(which is why this repo and others like it exist). Instead the data has been pre-feature-extracted using Google's own VGG-ish network \cite{}, the output for whch is a 128-dimentional feature vector for every second of a given sample(1Hz).
- In the bulk of the meta data supplied with the set that enables us to scrape it from YouTube, the classes are not labelled by name of event, but instead by some id. Id -> class name conversions are/can be done using the 'ontology.json' file.
- Estimated qualities of sound events are given in the form of true counts per some number of samples form a given class. This additional level of evaluation appears to manual with a true count representeing the event appearing within a class sample, e.g if 8 out of 10 samples in some class contained teh event it should it would have an 80% estimated quality.


## Basic Download Details

## Different Scripts

## Reproducibility & Exceptions

## Possible Issues
Is possible for YouTube to throttle access to their site after too many access requests. There are a few potential ways around this, these are:
- Setting some fixed time delay between downloads. This is very simple to set in the main control YAML file however comes with the caviat of significantly slowing down the full download process.
- Adding a cookies.txt file to the main script folder using your own YouTube and/or Google credentials. This is a bit more involved to set up however should allow the downoad to continue at normal speed. How to do this is covered in the Section  [Using A Cookies File](#markdown-Using-A-Cookies-File).


## Meta-Learning Considerations

## Using A Cookies File

One of the methods of getting around YouTube's 'Too Many Requests' issue is to use a cookies file whihc contains your encoded personal Google Credentials for use in the YouTube-DL package. This can be done by following these steps:
- Add the following extension to a chromium based browser(i.e Edge, Chrome etc) [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg). This extension helps collect the cookie data from the websites that have been used.
- Open Google or Youtube in a new tab and sign into an account.
- In this same tab Click the EditThisCookie extension and navigate to the top bar. Click the export button (5th from the left in my current version), this will copy the cookies needed into the clipboard.
- Paste this data into a new .txt file and save it as 'cookies.txt'
- Place this file in the main script directory.





## References
