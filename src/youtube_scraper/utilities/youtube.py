# ----- Python Standard Library -----
import random
import time

# ----- External Dependencies -----
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from thefuzz import fuzz

watched = []
dont_click = []


def search_for_term(logger, driver, search_term):
    # locate search bar
    for num, index in enumerate(range(1, 6), 1):
        try:
            search_bar = WebDriverWait(driver, timeout=5).until(
                EC.element_to_be_clickable((By.NAME, "search_query"))
            )
            break
        except:
            if num == 5:
                logger.critical("Attempt 5/5 - Could not locate search bar")
                raise Exception("Search bar could not be located, restarting script")
            logger.error(
                f"Attempt {num}/5 - A problem occured finding search bar, retrying"
            )
    # use search bar to look for term
    for num, index in enumerate(range(1, 6), 1):
        try:
            search_bar.clear()
            search_bar.send_keys(search_term)
            search_bar.send_keys(Keys.RETURN)
            WebDriverWait(driver, timeout=5).until(EC.title_contains(search_term))
            logger.info(f"Conducting search for {search_term}")
            break
        except:
            if num == 5:
                logger.critical(
                    "Attempt 5/5 - Could not complete initial search, restarting script"
                )
                raise Exception(
                    "Could not complete initial search, raising exception to restart"
                )
            logger.error(
                f"Attempt {num}/5 - A problem occured on initial search, retrying"
            )
    # find search results and click the video
    for num, index in enumerate(range(1, 6), 1):
        try:
            search_results = driver.find_elements(
                By.CSS_SELECTOR, "ytd-video-renderer.ytd-item-section-renderer"
            )
            title_str = only_click_video(
                logger, driver, videos=search_results, related_click=False
            )
            break
        except:
            if num == 5:
                logger.critical("Attempt 5/5 - Could not click video result of search")
                raise Exception("Could not click search result, restarting")
            logger.error(
                f"Attempt {num}/5 - A problem occured clicking search result, retrying"
            )
    return title_str


def find_related_video(driver, logger, search_term, title_str):
    # Get related videos
    for num, index in enumerate(range(1, 6), 1):
        related_videos = []
        # Set up retry
        while len(related_videos) < 10:
            # Find all related videos now that they've rendered
            related_videos = driver.find_elements(
                By.TAG_NAME, "ytd-compact-video-renderer"
            )
            # Give time for related videos to render
            if len(related_videos) < 10:
                # Return None and add to don't click if no related videos
                if num == 5:
                    dont_click.append(title_str)
                    return None
                # Else, wait 2 seconds for load
                time.sleep(2)
    # Parse through related videos for something related above the cutoff
    highest_ratio = 0
    chosen_title = None
    for video in related_videos:
        try:
            # Get the video title in parseable format
            title = video.find_element(By.ID, "video-title").text
            # Check likeness to the search term
            likeness = fuzz.partial_token_sort_ratio(search_term, title)
            # see if likeness is the highest
            if (
                likeness > highest_ratio
                and likeness > 50
                and title not in watched
                and title not in dont_click
            ):
                highest_ratio = likeness
                chosen_title = title
        # Pass to next video if object reference is stale
        except:
            pass
    if chosen_title == None:
        logger.info(
            "No related title with at least 50 percent match, restarting search"
        )
    else:
        logger.info(
            f"Selected {chosen_title} with {highest_ratio} likeness for the next click"
        )
    return chosen_title


def only_click_video(logger, driver, videos=None, related_click=False, title_str=None):
    if related_click == False:  # if first search and click, click a random video
        for num, index in enumerate(range(1, 6), 1):
            try:
                valid_video_found = False
                while not valid_video_found:
                    random_index_max = len(videos) - 1
                    random_vid = random.randint(0, random_index_max)
                    chosen_video = videos[random_vid]
                    chosen_title = chosen_video.find_element(
                        By.ID, "video-title"
                    )  # get video title
                    title_str = chosen_title.text
                    if title_str not in watched and title_str not in dont_click:
                        valid_video_found = True
                        logger.info(f"Selected video {title_str}, clicking")
                break
            except:
                if num == 5:
                    logger.error(
                        "Attempt 5/5 - Could not pick a random video from results passed, raising error to re-grab list"
                    )
                    raise AttributeError  # TODO Create custom error types (though it's not in logs so it doesn't REALLY matter)
                logger.warn(
                    f"Attempt {num}/5 - A problem occured picking a random video title, retrying with current list"
                )

    else:  # if clicking related video, process provided video titles to click best fit
        for num, index in enumerate(range(1, 6), 1):
            try:
                titles = driver.find_elements(
                    By.XPATH, f"//a/h3/span[@id='video-title']"
                )
                for title in titles:
                    if title.text == title_str:
                        chosen_title = title.find_element(By.XPATH, "../..")
                break
            except Exception as e:
                print("EXCEPTION")
                print(e)
                if num == 5:
                    logger.error(
                        "Attempt 5/5 - Could not locate related video by title, restarting script"
                    )
                    raise Exception("Could not locate selected related video")
                logger.warn(
                    f"Attempt {num}/5 - A problem ocured locating the related video by title, retrying"
                )

    for num, index in enumerate(range(1, 6), 1):  # get link of video
        try:
            link = chosen_title.get_attribute("href")
            break
        except Exception as e:
            if num == 5:
                logger.error(
                    "Attempt 5/5 - Could not get the link of the chosen video, raising error to re-grab list"
                )
                raise AttributeError  # TODO Create custom error types (though it's not in logs so it doesn't REALLY matter)
            logger.warn(
                f"Attempt {num}/5 - A problem occured getting the video link, regrabbing element to retry"
            )
            if related_click == False:
                chosen_title = driver.find_element(
                    By.XPATH, f"//a/yt-formatted-string[text()='{title_str}']"
                )
            else:
                titles = driver.find_elements(
                    By.XPATH, f"//a/h3/span[@id='video-title']"
                )
                for title in titles:
                    if title.text == title_str:
                        chosen_title = title.find_element(By.XPATH, "../..")

    if "watch" in link:  # check the link to see if it's a video
        for num, index in enumerate(range(1, 6), 1):
            try:  # try to click thumbnail if it is a video
                WebDriverWait(driver, timeout=5).until(
                    EC.element_to_be_clickable(chosen_title)
                )
                chosen_title.click()
                break
            except:  # re-grab title if unable to click due to possible stale element
                if num == 5:
                    logger.error(
                        "Attempt 5/5 - Could get the link of the chosen video, raising error to re-grab list"
                    )
                    raise AttributeError  # TODO Create custom error types (though it's not in logs so it doesn't REALLY matter)
                logger.warn(
                    f"Attempt {num}/5 - A problem occured getting the video link, regrabbing element to retry"
                )
                chosen_title = driver.find_element(
                    By.XPATH, f"//a/yt-formatted-string[text()='{title_str}']"
                )
    else:
        logger.info(
            "Random video selected was not a valid video, raising error to retry"
        )
        dont_click.append(title_str)
        raise Exception("Video was invalid, retry")

    # Re-Do if video was unavailable, add to do not click list, and retry
    try:
        WebDriverWait(driver, 10).until(EC.title_contains(title_str))
        watched.append(title_str)
        return title_str
    except:
        dont_click.append(title_str)
        raise Exception("video likely unavailable")


def get_video_object(driver, logger, title_str):
    for num, index in enumerate(range(1, 6), 1):
        try:
            WebDriverWait(driver, timeout=5).until(
                EC.visibility_of_element_located((By.ID, "movie_player"))
            )
            response = driver.execute_script(
                'return document.getElementById("movie_player")?.getPlayerResponse()'
            )
            return response
        except:
            if num == 5:
                logger.error(
                    "Attempt 5/5 - Could not get the video object, adding to do not click list to try again"
                )
                dont_click.append(title_str)
                driver.back()
                raise AttributeError  # TODO Create custom error types (though it's not in logs so it doesn't REALLY matter)
            logger.warn(
                f"Attempt {num}/5 - A problem occured getting the video object, retrying"
            )


def reset_globals():
    global watched
    global dont_click
    watched = []
    dont_click = []
