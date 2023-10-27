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
from math import trunc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----- Internal Dependencies -----
from youtube_scraper.utilities.driver import start_webdriver, check_for_driver
from youtube_scraper.utilities.youtube import search_for_term, get_video_object, find_related_video, only_click_video, reset_globals
from youtube_scraper.utilities.video_processing import find_index, process_data, determine_ad_length

# ----- Environment Setup -----
#set up tracking vars
downloaded_ads = 0
new = 0
duplicates = 0
clicks = 0

# Currently this file is set up to mirror the monitor function of the script, to try to locate
# information that does not exist in th emetadata pulled through the script provided by Matt


# ----- Monitor Script -----
def test(logger, time_target, profile):
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

    # Set driver to none for first run so that it gets opened
    driver = None 

    # For each search term
    for search in search_terms:

        # Start Timer
        end_time = datetime.now() + timedelta(minutes=time_per_search)

        # Set related video to none to start
        related_video = None

        # Reset global vars to empty lists
        reset_globals()
        logger.info(f"Reset global variables, conducting search: {search}")

        # While within timer
        while datetime.now() < end_time:

            try:
                # Open up web browser with provided profile if one is not open already
                if not check_for_driver(driver):
                    for num, index  in enumerate(range(1, 6)):
                        try:
                            driver = start_webdriver(profile)
                            logger.info("Webdriver successfully started")
                            break
                        except Exception as e:
                            if num == 5:
                                logger.critical(
                                    "Attempt 5/5 - Could not start webdriver"
                                )
                                raise Exception("Couldn't start driver, shutting down to restart")
                            logger.error(
                                f"Attempt {num}/5 - A problem occured starting the webdriver, retrying"
                            )

                match related_video:
                    case None:
                        for num, index in enumerate(range(1, 6)):
                            try:
                                # Set current date
                                date = datetime.now(tz=timezone("MST")).date()
                                # Make Search and Click Vid
                                title_str = search_for_term(logger, driver, search)
                                clicks += 1
                                # Collect initial video start
                                video_obj = get_video_object(driver, logger, title_str)
                                break
                            except Exception as e:
                                logger.debug(e)
                                if num == 5:
                                    logger.error(
                                        "Attempt 5/5 - Could not grab first video data"
                                    )
                                    raise Exception("Couldn't get first video, shutting down to restart")
                                logger.warn(
                                    f"Attempt {num}/5 - A problem occured grabbing first video data, retrying"
                                )

                        # Save JSON file for testing
                        with open("videoObj_0.json", "w") as file:
                            json.dump(video_obj, file)

                        # Start Timer
                        parse_start = datetime.now()

                        # Parse the video object for ads 
                        ad_index, new_processed, duplicates_processed, length, ad_presence = process_data(video_obj, ad_index, clicks, search, profile, date)

                        # Update globals
                        new += new_processed
                        duplicates += duplicates_processed

                        # Parse through titles of related videos for like videos
                        related_video = find_related_video(driver, logger, search, title_str)

                        # Determine Ad Length
                        if ad_presence:
                            length_of_ads = determine_ad_length(video_obj)
                        else:
                            length_of_ads = 0

                        # End Timer
                        parse_end = datetime.now()

                        # Math out how long to wait and wait
                        total_time = length + length_of_ads
                        delta = parse_end - parse_start
                        until_end_of_vid = trunc(total_time - delta.total_seconds() - 5) #reduce an extra 5 seconds as buffer
                        if until_end_of_vid > 1200:
                            until_end_of_vid = 1200
                        logger.info(f"Waiting {until_end_of_vid} seconds until video is 5 seconds from over.")

                        print("Testing portion now")
                        # Wait until video is close to over
                        current_time = datetime.now()
                        wait_until = current_time + timedelta(seconds=until_end_of_vid)
                        historical = ""
                        times_changed = 1
                        while datetime.now() < wait_until:
                            #see if ads are running
                            # TODO Use code from previous branch (https://github.com/Appologetic/YouTube_Scraper/blob/f0e2d5113609fc2fe3c6386df3803317b28e4aeb/youtube_scraper/scrape.py) to take metadata of mid-post roll ads
                            try:
                                driver.find_element(By.CSS_SELECTOR, "div.ytp-ad-player-overlay")
                                current = "present"
                                print("ads present")
                            except:
                                print("ads absent")
                                current = "absent"
                            if current != historical:
                                print("Change detected!")
                                video_obj = get_video_object(driver, logger, title_str)
                                with open(f"videoObj_{times_changed}.json", "w") as file:
                                    json.dump(video_obj, file)
                                times_changed += 1
                            historical = current
                            time.sleep(5)

                    case _:
                        try:
                            # Find and click chosen related video
                            title_str = only_click_video(logger, driver, related_click=True, title_str=related_video)
                            clicks += 1


                            # Get video object
                            video_obj = get_video_object(driver, logger, title_str)

                            # Save JSON file for testing
                            with open("videoObj_0.json", "w") as file:
                                json.dump(video_obj, file)

                            # Start Timer
                            parse_start = datetime.now()

                            # Parse the video object for ads 
                            ad_index, new_processed, duplicates_processed, length, ad_presence = process_data(video_obj, ad_index, clicks, search, profile, date)

                            # Update globals
                            new += new_processed
                            duplicates += duplicates_processed

                            # Parse through titles of related videos for like videos
                            related_video = find_related_video(driver, logger, search, title_str)

                            # Determine Ad Length
                            if ad_presence:
                                length_of_ads = determine_ad_length(video_obj)
                            else:
                                length_of_ads = 0

                            # End Timer
                            parse_end = datetime.now()

                            # Math out how long to wait and wait
                            total_time = length + length_of_ads
                            delta = parse_end - parse_start
                            until_end_of_vid = trunc(total_time - delta.total_seconds() - 5) #reduce an extra 5 seconds as buffer
                            if until_end_of_vid > 1200:
                                until_end_of_vid = 1200
                            logger.info(f"Waiting {until_end_of_vid} seconds until video is 5 seconds from over.")

                            print("testing poriton now")
                            # Wait until video is close to over
                            current_time = datetime.now()
                            wait_until = current_time + timedelta(seconds=until_end_of_vid)
                            historical = ""
                            times_changed = 1
                            while datetime.now() < wait_until:
                                #see if ads are running
                                try:
                                    driver.find_element(By.CSS_SELECTOR, "div.ytp-ad-player-overlay")
                                    current = "present"
                                    print("ads present")
                                except:
                                    print("ads absent")
                                    current = "absent"
                                if current != historical:
                                    print("Change detected!")
                                    video_obj = get_video_object(driver, logger, title_str)
                                    with open(f"videoObj_{times_changed}.json", "w") as file:
                                        json.dump(video_obj, file)
                                    times_changed += 1
                                historical = current
                                time.sleep(5)

                        # If we error anywhere, just reset search
                        except Exception as e:
                            logger.debug(e)
                            related_video = None
            
            #if we error out, quit and restart from scratch with current search
            except Exception as e:
                if check_for_driver(driver):
                    logger.info(f"Error occured - {e}")
                    driver.quit()
                pass

    # Print end statement
    logger.info(f"""Finished monitoring for {time_target} hours. During this monitoring session, we located:
                {duplicates} - Duplicate Ads
                {new} - New Ads
                """)
    print(f"""Finished monitoring for {time_target} hours. During this monitoring session, we located:
            {duplicates} - Duplicate Ads
            {new} - New Ads
            """)
    exit(1)
