# M2K YouTube Ad Scraper
## A command line tool written in Python to find and index YouTube Ads
As part of the M2K project at the University of Calgary, we will create a machine-learning model to process text, image, and video advertisements and determine if they advertise unhealthy food items to children. The first step in this process is the collection of many ads of all shapes and sizes to train our model. We've designed this script to be a user-friendly and simple means of obtaining ads from YouTube, a content distributor frequently visited by many children and that often serves ads to them.

### Features and How it Works
We've designed the scraper to use a web browser to mimic a real user's behavior on YouTube to find advertisements with which to train our machine-learning model. The script will first prompt you to provide a search term and a number of ads you'd like to download. A web browser will then open and search YouTube for your entered search term, clicking on a random video provided by the search and continuing to click related videos until it finds an ad. Once it sees an ad, the script will save it locally as an MP4 file named after the video ID of the ad assigned by YouTube. For instance, the script would download this Wix ad to a folder titled /downloaded_ads in the working directory as S6uoq-8jOl0.mp4. In addition, the script will create an index CSV containing metadata about the ad, such as how many related videos in the initial search the ad was found and the URL of the video it was found on. The script will then continue to click random related videos until another ad is located and will continue to do so until the number of ads downloaded matches the target you provided.

By creating a script that takes user inputs for search and the number of ads you'd like to download, this project aims to be versatile and efficient in compiling a large number of relevant ads quickly and efficiently to fit the needs of any project.

### Pre Reqs
##### 1. Python 3.7 or Higher
We've written this tool in Python 3.10. However, there should be no issues running it in Python 3.7, though we've yet to test this fully. If you don't have Python installed on your computer, please visit the [official Python website](https://www.python.org/downloads/) to download and install the most recent stable release.

If you run into any issues running the script with a specific version of Python, please submit an issue so we can investigate the problem and resolve it. To do so, please see the ["Issues and Features"](#issues/feature-contributions) section of the README.

##### 2. A Chrome Web Driver Added to System PATH
The scraper uses [Selenium](https://pypi.org/project/selenium/) to instantiate a web browser and send keys/actions to locate YouTube ads. The script assumes that a Chrome web driver has been downloaded and is accessible via the system PATH.  To do so, visit [the ChromeDriver downloads page](https://chromedriver.chromium.org/downloads) to download the version of the driver for your system, and follow online directions for [windows/mac](https://zwbetz.com/download-chromedriver-binary-and-add-to-your-path-for-automated-functional-testing/) or [linux](https://www.browserstack.com/guide/run-selenium-tests-using-selenium-chromedriver#:~:text=Go%20to%20the%20terminal%20and,Type%20Y%20to%20save) before running the script.

**Please Note:** This step may not be required in the future, as there are packages that allow scripts like this to install/check for installations on the user's machine.Check [this issue](https://github.com/Appologetic/YouTube_Scraper/issues/7) for updates on when we've completed work on this feature.

### Installation
We've included a pyproject.toml with up-to-date dependencies for easy installation with pip. To install the script, first download the code/clone the directory to your machine, and run the following command in the root directory of the repository:
```
pip install .
```
Pip will then install the script to your PATH and all the required package dependencies without needing anything further on your part. Once the installation is complete, you're ready to use the script!

### How To Use
We've designed the tool to be as user-friendly as possible and do not require ANY code/file editing. To start, open a terminal and move to whichever directory you'd like to have the downloaded_ads folder created in. For instance, if you'd like this folder of ads on your desktop, ensure that the working directory is on the desktop as it is below:
```
C:\Users\sfietz\Desktop>
```
Once you've ensured your working directory is correct, run the command "scrape" to start the interactive tool.
```
C:\Users\sfietz\Desktop> scrape
```
From there, the script will ask you to provide the search term you'd like it to use to look for ads and how many ads you'd like to download. When prompted, provide the script with the required field and hit "Enter" to proceed. The script will then run and search for ads under the search term provided and will automatically exit when it's reached the target!

### GitHub Issues for Feature Requests, Bug Reports and Questions
We're currently working on setting up issue templates for these fields! Check back here in the future for info on how to use GitHub issues to submit requests, questions and report bugs.

### Current Versions New Features
This is the first version of the script! Please check back here for new additions in the future!
