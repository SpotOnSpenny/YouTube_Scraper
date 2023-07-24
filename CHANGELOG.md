# 0.0.1 (2023-06-10)

## About this version

- Search currently ignores all ads and shorts that come up on search
  - Later could add in a download if there is an ad displayed with search
  - Later could add in logic for channel/short clicks
    - For now, elected against it for simplicity for proof of concept
- Search currently displays all videos that displays on page 1 of results
  - Later could scroll a random number of times to load more videos and then search
    - Elected against this for first try, most people will likely click one of the first few results
    - Later could even weight the randomness so that first few links are more likely to be clicked
- Search currently randomly selects a video on search
  - Later could likely add some sort of thumbnail processing to select image that children would be more likely to click on, or weight these videos as more likely to be clicked
- Search currently clicks videos until an ad is found and then downloads that ad to the /youtube_scraper/donwloaded_ads directory
  - Youtube stops showing ads for a while after a bit. May be good to have a wait for 30 seconds to register a view before continuing, or restart if ads not found after certain number of videos
  - This is not NEEDED, as ads will start showing again after a while, but may help to optimize the number of ads we can find
    -Current rate is ~7 ads over 10 minutes

# 0.0.2 (2023-06-26)

## About this Version

- Added function to scrape multiple ads on a single video
  - When youtube shows an ad, it typically does so in groups of 2-3
  - As of 0.0.2 the script now checks to see how many ads are served, and will wait for the next ad to display if the current ad is under a minute long

# 0.0.4 (2023-07-24)

## About this Version

- Added the ability to scrape data using existing profile data
- Search will now restart if 50 videos are processed without any ads being displayed, this drops processing time down to ~10 ads per minute
  - This is a HUGE increase in processing time (14x to be exact!)
- Refactored codebase so that it's easier to develop on top of in the future to add extra features
- Added colored print statements to make it easier to see when an add is found/added
- Scrape is now timed to give a better idea on how fast you are able to find the ads
  - This feature will be used in the future to further optimize the script
- Instead of using the DOM to find info about the ad, a script is now run which returns the video player object which contains information about all ads served
  - Removes the logic required previously to wait for a second ad as now all ads on the video can be found in one go
  - Also no need to right click the video in order to find tha ad ID, overall much cleaner
  - Thanks, Matt!
