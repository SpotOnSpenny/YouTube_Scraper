# ----- External Dependencies -----
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----- Python Standard Library -----
import os
from datetime import datetime, timedelta
import json
from itertools import chain
import time
from pytz import timezone
from math import trunc

# ----- Internal Dependencies -----
from youtube_scraper.utilities.driver import start_webdriver, check_for_driver
from youtube_scraper.utilities.youtube import (
    search_for_term,
    get_video_object,
    find_related_video,
    only_click_video,
    reset_globals,
)
from youtube_scraper.utilities.video_processing import (
    find_index,
    process_data,
    determine_ad_length,
    id_mid_post,
    process_mid_post,
)

# ----- Environment Setup -----
# set up tracking vars
downloaded_ads = 0
new = 0
duplicates = 0
clicks = 0


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
                    for num, index in enumerate(range(1, 6), 1):
                        try:
                            driver, action = start_webdriver(profile)
                            logger.info("Webdriver successfully started")
                            break
                        except Exception as e:
                            if num == 5:
                                logger.critical(
                                    "Attempt 5/5 - Could not start webdriver"
                                )
                                raise Exception(
                                    "Couldn't start driver, shutting down to restart"
                                )
                            logger.error(
                                f"Attempt {num}/5 - A problem occured starting the webdriver, retrying"
                            )

                match related_video:
                    case None:
                        for num, index in enumerate(range(1, 6), 1):
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
                                    raise Exception(
                                        "Couldn't get first video, shutting down to restart"
                                    )
                                logger.warn(
                                    f"Attempt {num}/5 - A problem occured grabbing first video data, retrying"
                                )

                        # Start Timer
                        parse_start = datetime.now()

                        # Parse the video object for ads
                        (
                            ad_index,
                            new_processed,
                            duplicates_processed,
                            length,
                            ad_presence,
                            ad_metadata,
                        ) = process_data(
                            video_obj, ad_index, clicks, search, profile, date
                        )

                        # Update globals
                        ads_on_video = new_processed + duplicates_processed
                        new += new_processed
                        duplicates += duplicates_processed

                        # Parse through titles of related videos for like videos
                        related_video = find_related_video(
                            driver, logger, search, title_str
                        )

                        # Determine Ad Length
                        if ad_presence:
                            length_of_ads = determine_ad_length(video_obj)
                            # Wait an extra 20 seconds in case any ads have an end of ad CTA screen
                            length_of_ads += 20
                        else:
                            length_of_ads = 0

                        # End Timer
                        parse_end = datetime.now()

                        # Math out how long to wait and wait
                        delta = parse_end - parse_start
                        until_end_of_vid = trunc(
                            length - delta.total_seconds() - 5
                        )  # reduce an extra 5 seconds as buffer
                        if until_end_of_vid > 1200:
                            until_end_of_vid = 1200
                        logger.info(
                            f"Waiting {until_end_of_vid} seconds until next video."
                        )

                        # wait for pre-roll ads to be over
                        time.sleep(length_of_ads)

                        # Wait until video is close to over, check for ads consistently while waiting
                        current_time = datetime.now()
                        wait_until = current_time + timedelta(seconds=until_end_of_vid)
                        while datetime.now() < wait_until:
                            # see if ads are running
                            try:
                                WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located(
                                        (By.CSS_SELECTOR, "div.ytp-ad-player-overlay")
                                    )
                                )

                                # try to find multiple ads if they are running
                                try:
                                    number_of_ads = driver.find_element(
                                        By.CLASS_NAME, "ytp-ad-simple-ad-badge"
                                    ).text.split()
                                    ads_served = int(number_of_ads[3])

                                    # find which ad we're on now
                                    current_ad = int(
                                        driver.find_element(
                                            By.CLASS_NAME, "ytp-ad-simple-ad-badge"
                                        ).text.split()[1]
                                    )
                                # if an error occurs splitting, then just assume 1 ad served
                                except:  # Except may not be needed, need to see what 1 ad looks like
                                    ads_served = 1
                                    current_ad = 1

                                process_or_not = True

                                # process each ad
                                while current_ad <= ads_served:
                                    if process_or_not:
                                        #double check to ensure that the ad ID has changed to a new ad
                                        valid_id = False
                                        previous_id = None
                                        while not valid_id:
                                            #check 5 times to see if the ad_id we get is empty
                                            for n, index in enumerate(range(1,6), 1):
                                                ad_id, ad_endpoint = id_mid_post(
                                                    driver, action
                                                )
                                                if ad_id != "empty_video":
                                                    break
                                                else:
                                                    time.sleep(1)

                                            if ad_id != previous_id:
                                                valid_id = True
                                                previous_id = ad_id

                                        # process new ads and add to spreadsheet
                                        (
                                            ad_index,
                                            new_processed,
                                            duplicates_processed,
                                        ) = process_mid_post(
                                            ad_index, ad_id, ad_endpoint, ad_metadata
                                        )

                                        # update globals
                                        new += new_processed
                                        duplicates += duplicates_processed
                                        ads_on_video += (
                                            new_processed + duplicates_processed
                                        )

                                        # update search vars
                                        next_ad = current_ad + 1
                                        next_ad_text = f"{next_ad} of {ads_served}"

                                        # set not process while we wait for next ad
                                        process_or_not = False

                                    # wait for ad to change to next, and restart loop
                                    try:
                                        WebDriverWait(driver, 5).until(
                                            EC.text_to_be_present_in_element(
                                                (
                                                    By.CLASS_NAME,
                                                    "ytp-ad-simple-ad-badge",
                                                ),
                                                next_ad_text,
                                            )
                                        )
                                        process_or_not = True
                                        current_ad += 1
                                    # skip directly to waiting if ad doesn't change over in time
                                    except:
                                        # break the loop if we've hit the end
                                        if current_ad == ads_served:
                                            current_ad += 1

                                # wait for ad to stop being shown before we resume scanning for another
                                ad_showing = True
                                while ad_showing:
                                    try:
                                        # if ad showing, wait 5 seconds and look again
                                        driver.find_element(
                                            By.CSS_SELECTOR, "div.ytp-ad-player-overlay"
                                        )
                                        time.sleep(5)
                                    except:
                                        ad_showing = False
                                        pass

                            except:
                                pass

                        # log how many ads found on the video before
                        logger.info(
                            f"{ads_on_video} ads were found on this video, moving onto the next video now."
                        )

                    case _:
                        try:
                            # Find and click chosen related video
                            title_str = only_click_video(
                                logger,
                                driver,
                                related_click=True,
                                title_str=related_video,
                            )
                            clicks += 1

                            # Get video object
                            video_obj = get_video_object(driver, logger, title_str)

                            # Start Timer
                            parse_start = datetime.now()

                            # Parse the video object for ads
                            (
                                ad_index,
                                new_processed,
                                duplicates_processed,
                                length,
                                ad_presence,
                                ad_metadata,
                            ) = process_data(
                                video_obj, ad_index, clicks, search, profile, date
                            )

                            # Update globals
                            new += new_processed
                            duplicates += duplicates_processed
                            ads_on_video = new_processed + duplicates_processed

                            # Parse through titles of related videos for like videos
                            related_video = find_related_video(
                                driver, logger, search, title_str
                            )

                            # Determine Ad Length
                            if ad_presence:
                                length_of_ads = determine_ad_length(video_obj)
                                # add 20 seconds extra in case any of the ads have the ending CTA screen
                                length_of_ads += 20
                            else:
                                length_of_ads = 0

                            # End Timer
                            parse_end = datetime.now()

                            # Math out how long to wait and wait
                            delta = parse_end - parse_start
                            until_end_of_vid = trunc(
                                length - delta.total_seconds() - 5
                            )  # reduce an extra 5 seconds as buffer
                            if until_end_of_vid > 1200:
                                until_end_of_vid = 1200
                            logger.info(
                                f"Waiting {until_end_of_vid} seconds until next video."
                            )

                            # wait for pre-roll ads to be over
                            time.sleep(length_of_ads)

                            # Wait until video is close to over, check for ads consistently while waiting
                            current_time = datetime.now()
                            wait_until = current_time + timedelta(
                                seconds=until_end_of_vid
                            )
                            while datetime.now() < wait_until:
                                # see if ads are running
                                try:
                                    WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located(
                                            (
                                                By.CSS_SELECTOR,
                                                "div.ytp-ad-player-overlay",
                                            )
                                        )
                                    )

                                    # try to find multiple ads if they are running
                                    try:
                                        number_of_ads = driver.find_element(
                                            By.CLASS_NAME, "ytp-ad-simple-ad-badge"
                                        ).text.split()
                                        ads_served = int(number_of_ads[3])
                                    except:  # Except may not be needed, need to see what 1 ad looks like
                                        ads_served = 1

                                    # find which ad we're on now
                                    current_ad = int(
                                        driver.find_element(
                                            By.CLASS_NAME, "ytp-ad-simple-ad-badge"
                                        ).text.split()[1]
                                    )
                                    process_or_not = True

                                    # process each ad
                                    while current_ad <= ads_served:
                                        if process_or_not:
                                            #double check to ensure that the ad ID has changed to a new ad
                                            valid_id = False
                                            previous_id = None
                                            while not valid_id:
                                                #check 5 times to see if the ad_id we get is empty
                                                for n, index in enumerate(range(1,6), 1):
                                                    ad_id, ad_endpoint = id_mid_post(
                                                        driver, action
                                                    )
                                                    if ad_id != "empty_video":
                                                        break
                                                    else:
                                                        time.sleep(1)

                                                if ad_id != previous_id:
                                                    valid_id = True
                                                    previous_id = ad_id

                                            # get ad ID and endpoint
                                            ad_id, ad_endpoint = id_mid_post(
                                                driver, action
                                            )

                                            # process new ads and add to spreadsheet
                                            (
                                                ad_index,
                                                new_processed,
                                                duplicates_processed,
                                            ) = process_mid_post(
                                                ad_index,
                                                ad_id,
                                                ad_endpoint,
                                                ad_metadata,
                                            )

                                            # update globals
                                            new += new_processed
                                            duplicates += duplicates_processed
                                            ads_on_video += (
                                                new_processed + duplicates_processed
                                            )

                                            # update search vars
                                            next_ad = current_ad + 1
                                            next_ad_text = f"{next_ad} of {ads_served}"

                                            # set not process while we wait for next ad
                                            process_or_not = False

                                        # wait for ad to change to next, and restart loop
                                        try:
                                            WebDriverWait(driver, 5).until(
                                                EC.text_to_be_present_in_element(
                                                    (
                                                        By.CLASS_NAME,
                                                        "ytp-ad-simple-ad-badge",
                                                    ),
                                                    next_ad_text,
                                                )
                                            )
                                            process_or_not = True
                                            current_ad += 1
                                        # skip directly to waiting if ad doesn't change over in time
                                        except:
                                            # break the loop if we've hit the end
                                            if current_ad == ads_served:
                                                current_ad += 1

                                    # wait for ad to stop being shown before we resume scanning for another
                                    ad_showing = True
                                    while ad_showing:
                                        try:
                                            # if ad showing, wait 5 seconds and look again
                                            driver.find_element(
                                                By.CSS_SELECTOR,
                                                "div.ytp-ad-player-overlay",
                                            )
                                            time.sleep(5)
                                        except:
                                            ad_showing = False
                                            pass

                                except:
                                    pass

                            # log how many ads found on the video before
                            logger.info(
                                f"{ads_on_video} ads were found on this video, moving onto the next video now."
                            )

                        # If we error anywhere, just reset search
                        except Exception as e:
                            logger.debug(e)
                            related_video = None

            # if we error out, quit and restart from scratch with current search
            except Exception as e:
                if check_for_driver(driver):
                    logger.info(f"Error occured - {e}")
                    driver.quit()
                pass

    # Print end statement
    logger.info(
        f"""Finished monitoring for {time_target} hours. During this monitoring session, we located:
                {duplicates} - Duplicate Ads
                {new} - New Ads
                """
    )
    print(
        f"""Finished monitoring for {time_target} hours. During this monitoring session, we located:
            {duplicates} - Duplicate Ads
            {new} - New Ads
            """
    )
    exit(1)
