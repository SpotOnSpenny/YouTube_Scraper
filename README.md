# M2K YouTube Ad Scraper
## A command line tool written in Python to find and index YouTube Ads
As part of the M2K project at the University of Calgary a machine learning model will be created to process text, image and video advertisements and determine if they are advertising unhealthy food items to children. In order to train this model, a mass amount of ads of all shapes and sizes must be obtained in order to train. This script is designed to be a user friendly, and simple means of obtaining ads from YouTube, a content distributor frequently visited by many children, and which frequently serves ads to them.

### Features and How it Works
The scraper is designed in a way which uses a web browser to mimic a real users behavour on YouTube in order to find advertisements with which to train our machine learning model. To do so, you will be asked to provide the script with a search term and a number of ads you'd like to download. A web browser will then open and search YouTube for your entered search term, clicking on a random video provided by the search, and continuing to click related videos until an ad is found. Once an ad is found, it gets saved locally as an MP4 file named after the video ID of the ad assigned by YouTube. For instance, [this Wix ad](https://youtube.com/watch?v=S6uoq-8jOl0) would be downloaded to a folder titled /downloaded_ads in the working directory as S6uoq-8jOl0.mp4. In addition to this, the script will also create an index CSV containing metadata about the ad such as how many related videos into the initial search the ad was found, and the URL of the video it was found on. The script will then continue to click random related videos until another ad is found and will continue to do so until the number of ads downloaded match the target that you provided it.

By creating a script that takes user inputs for search and number of ads you'd like to download, this project aims to be versitile and efficient in compiling a large amount of relevant ads quickly and efficiently to fit the needs of any project.

### Pre Reqs
##### 1. Python 3.7 or Higher
The script was written in Python 3.10, however there shouldn't be any issues running it in Python 3.7, though this hasn't been fully tested. If you don't have Python installed on your computer, please visit the [official Python website](https://www.python.org/downloads/) to download and install the most recent stable release.

If you run into any issues running the script with a specific version of Python, please submit an issue so that we can investigate the problem and resolve it. To do so, please see the ["Issues and Features"](#issues/feature-contributions) section of the README.

##### 2. A Chrome Web Driver Added to System PATH
The scraper uses [Selenium](https://pypi.org/project/selenium/) to instantiate a web browser and send keys/actions to it to locate YouTube ads. In order to do so, the script assumes that a chrome web driver has been downloaded and is accessible via the system PATH. To do so, visit [the ChromeDriver downloads page](https://chromedriver.chromium.org/downloads) to download the version of the driver for your system, and follow online directions for [windows/mac](https://zwbetz.com/download-chromedriver-binary-and-add-to-your-path-for-automated-functional-testing/) or [linux](https://www.browserstack.com/guide/run-selenium-tests-using-selenium-chromedriver#:~:text=Go%20to%20the%20terminal%20and,Type%20Y%20to%20save) before running the script.

**Please Note:** This step may not be required in the future, as there are packages which allow scripts like this to install/check for installations on the users machine. Check [this issue](https://github.com/Appologetic/YouTube_Scraper/issues/7) for updates on when this will be implemented.

### Installation
A pyproject.toml has been included with up to date dependencies for easy installation with pip. To install the script, first download the code/clone the directory to your machine, and run the following command in the root directory of the repository:
```
pip install .
```
Pip will then install the script to your PATH, and will install all the required package dependancies without the need for anything further on your part. Once the install is complete, you're ready to use the script!

### How To Use
The script is designed to be as user friendly as possible, and as such does not require ANY code/file editing to operate. Simply open a terminal and move to whichever directory you'd like to have the downloaded_ads folder created in. For instance if you'd like this folder of ads to be created on your desktop, ensure that the working directory is on the desktop as it is below:
```
C:\Users\sfietz\Desktop>
```
Once you've ensured your working directory is correct, simply run the command "scrape" to run the script.
```
C:\Users\sfietz\Desktop> scrape
```
From there you'll be asked to provide the search term that you'd like the script to look for ads using, as well as how many ads you'd like to download. When prompted, provide the script with the required field and hit "Enter" to proceed. The script will then run and search for ads under the search term provided!

### GitHub Issues for Feature Requests, Bug Reports and Questions
Issue templates are currently being worked on! Check back here in the future for info on how to use GitHub issues to submit requests, questsions and report bugs.

### Current Versions New Features
This is the first version of the script! Please check back here for new additions in the future!
