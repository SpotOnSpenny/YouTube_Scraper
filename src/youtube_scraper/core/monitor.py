# ----- External Dependencies -----

# ----- Python Standard Library -----
import logging
from logging.handlers import SysLogHandler
import os
from datetime import datetime, timedelta
import json
from itertools import chain
import time

# ----- Internal Dependencies -----
from youtube_scraper.utilities.driver import start_webdriver
from youtube_scraper.utilities.youtube import search_for_term


# ----- Monitor Script -----
def monitor(logger, time_target, profile):
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

    # Math out how long to search for each term based on time_target
    time_per_search = round(time_target * 60 / len(search_terms))

    # Open up web browser with provided profile

    for num, index in enumerate(range(1, 6)):
        try:
            driver = start_webdriver(profile)
            logger.info("Webdriver successfully started")
            break
        except Exception as e:
            if num == 5:
                logger.critical(
                    "Attempt 5/5 - Could not start webdriver, exiting with error code 1"
                )
                exit(1)
            logger.error(
                f"Attempt {num}/5 - A problem occured starting the webdriver, retrying"
            )

    # For each search term
    for search in search_terms:
        # Start Timer
        end_time = datetime.now() + timedelta(minutes=time_per_search)
        while datetime.now() < end_time:
            # Start 10 Video Clock
            clicks_without_ads = 1

            # Make Search and Click Vid
            search_for_term(logger, driver, search)
            # collect initial video start


    # Start Processing Thread
    # Pass video object to thread
    # If no ads, then ad 1 to 10 video clock
    # If clock at 10, skip next step, set related video to None
    # If yes ads, then set clock to 0
    # If 10 video clock not at 10
    # Parse through titles of related videos for like videos
    # If one is found above threshold of like 65% (? maybe ask sara if she knows a way to make this significant) store title
    # If one not found, related video = None
    # Wait for video to be 5-20 seconds from ending
    # If related video = None
    # Click the search bar again and start over
    # Set 10 video clock to 0
    # Find element with related Click related video
    # Click the related video
    # Wait browser title to change
    # Start over
    exit(1)


# ----- run for testing -----
if __name__ == "__main__":
    monitor(None, 0.1, None)
