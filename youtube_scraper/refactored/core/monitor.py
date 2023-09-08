# ----- External Dependencies -----

# ----- Python Standard Library -----
import logging
from logging.handlers import SysLogHandler
import os
from datetime import datetime
import json

# ----- Internal Dependencies -----


# ----- Monitor Script -----
def monitor(logger, time_target, profile):
    # Locate json containing search terms
    dir_name = os.path.dirname(os.path.abspath(__file__))
    print(dir_name) # path to youtube_scraper folder on current machine
    with open(os.path.join(dir_name, "search_terms.json")) as search_terms_file:
        search_terms = json.load(search_terms_file)
    test = list(map(lambda json_data: json_data["search terms"] if json_data["profile"] == profile else None, search_terms))
    print(test)
    # Math out how long to search for each term based on time_target
    # For each search term
    # Start Timer
    # Start 10 Video Clock
    # Make Search
    # Click Video from Search
    # Start Processing Thread
    # While time on timer < time delta of how long to search from time start
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
    monitor(None, None, None)
