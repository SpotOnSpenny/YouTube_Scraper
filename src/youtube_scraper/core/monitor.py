# ----- External Dependencies -----

# ----- Python Standard Library -----
import logging
from logging.handlers import SysLogHandler
import os
from datetime import datetime, timedelta
import json
from itertools import chain
import time
from pytz import timezone

# ----- Internal Dependencies -----
from youtube_scraper.utilities.driver import start_webdriver
from youtube_scraper.utilities.youtube import search_for_term, get_video_object, find_related_video
from youtube_scraper.utilities.video_processing import find_index, process_data, determine_ad_length

# ----- Environment Setup -----
#set up tracking vars
downloaded_ads = 0
new = 0
duplicates = 0
clicks = 1


# ----- Monitor Script -----
def monitor(logger, time_target, profile):
    global new
    global duplicates
    global clicks
    # Locate json containing search terms
    dir_name = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_name, "search_terms.json")) as search_terms_file:
        search_terms = json.load(search_terms_file)

    # Create list of all search terms with matching profile to the one provided
    search_terms = list(
        chain.from_iterable(
            [
                dict["search terms"]
                for dict in search_terms
                if dict["profile"] == profile
            ]
        )
    )

    # Locate or create the dataframe to use and add ads to
    ad_index = find_index(logger)

    # Math out how long to search for each term based on time_target
    time_per_search = round(time_target * 60 / len(search_terms))

    # Open up web browser with provided profile
    for num, index  in enumerate(range(1, 6)):
        try:
            driver = start_webdriver(profile)
            logger.info("Webdriver successfully started")
            break
        except Exception as e:
            if num == 5:
                logger.critical(
                    "Attempt 5/5 - Could not start webdriver,  exiting with error code 1"
                )
                exit(1)
            logger.error(
                f"Attempt {num}/5 - A problem occured starting the webdriver, retrying"
            )

    # For each search term
    for search in search_terms:

        # Start Timer
        end_time = datetime.now() + timedelta(minutes=time_per_search)

        # Set related video to none to start
        related_video = None

        # While within timer
        while datetime.now() < end_time:
            match related_video:
                case None:
                    for num, index in enumerate(range(1, 6)):
                        try:
                            # Set current date
                            date = datetime.now(tz=timezone("MST")).date()
                            # Make Search and Click Vid
                            title_str = search_for_term(logger, driver, search)
                            # Collect initial video start
                            print("getting object")
                            video_obj = get_video_object(driver, logger, title_str)
                            break
                        except Exception as e:
                            print(e)
                            if num == 5:
                                logger.error(
                                    "Attempt 5/5 - Could not grab first video data, exiting"
                                )
                                exit(1)
                            logger.warn(
                                f"Attempt {num}/5 - A problem occured grabbing first video data, retrying"
                            )

                    # Start Timer
                    parse_start = datetime.now()

                    # Parse the video object for ads 
                    try:
                        ad_index, new_processed, duplicates_processed, length, ad_presence = process_data(video_obj, ad_index, clicks, search, profile, date)
                    except:
                        print("error processing")

                    # Update globals
                    new += new_processed
                    duplicates += duplicates_processed

                    # Parse through titles of related videos for like videos
                    try:
                        related_video = find_related_video(driver, search, title_str)
                        print(related_video)
                    except:
                        print("error finding related")

                    # Determine Ad Length
                    try:
                        if ad_presence:
                            length_of_ads = determine_ad_length(video_obj)
                            print(length_of_ads)
                    except Exception as e:
                        print("error determining ad length")
                        print(e)

                    # End Timer
                    parse_end = datetime.now()
                    exit(1)

                    # Wait for video to be 5-20 seconds from ending (remove processing time and timer from the video length)
                    

                case _:
                    # Find link for related video
                    exit(1)
                    # Click
                    # Wait for Title to Change
                    # Get Data and Process Again
                    # Parse through titles for related videos
                    # Store title above threshold to related video
    # Print end statement
    exit(1)


# ----- run for testing -----
if __name__ == "__main__":
    monitor(None, 0.1, None)
