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


def search_for_term(logger, driver, search_term):
    # locate search bar
    for num, index in enumerate(range(1, 6)):
        try:
            search_bar = WebDriverWait(driver, timeout=5).until(
                EC.element_to_be_clickable((By.NAME, "search_query"))
            )
            break
        except:
            if num == 5:
                logger.critical(
                    "Attempt 5/5 - Could not locate search bar, exiting with error code 1"
                )
                exit(1)
            logger.error(
                f"Attempt {num}/5 - A problem occured finding search bar, retrying"
            )
    # use search bar to look for term
    for num, index in enumerate(range(1, 6)):
        try:
            search_bar.send_keys(search_term)
            search_bar.send_keys(Keys.RETURN)
            WebDriverWait(driver, timeout=5).until(EC.title_contains(search_term))
            logger.info(f"Search for {search_term} complete")
            break
        except:
            if num == 5:
                logger.critical(
                    "Attempt 5/5 - Could not complete initial search, exiting with error code 1"
                )
                exit(1)
            search_bar.clear()
            logger.error(
                f"Attempt {num}/5 - A problem occured on initial search, retrying"
            )
    # find search results and click the video
    for num, index in enumerate(range(1, 6)):
        try:
            search_results = driver.find_elements(
                By.CSS_SELECTOR, "ytd-video-renderer.ytd-item-section-renderer"
            )
            only_click_video(logger, driver, search_results, False)
            break
        except:
            if num == 5:
                logger.critical("Attempt 5/5 - Could not click video result of search")
                exit(1)
            logger.error(
                f"Attempt {num}/5 - A problem occured clicking search result, retrying"
            )
    pass


def click_related_video(driver, search_term, do_not_click=[]):
    # get related videos
    i = 1
    related_videos = []
    while (
        len(related_videos) < 10 and i < 7
    ):  # wait for all related video items to render
        related_videos = driver.find_elements(
            By.TAG_NAME, "ytd-compact-video-renderer"
        )  # find all related video elements now that they've rendered
        if len(related_videos) < 10:
            time.sleep(2)
            i += 1
    if i >= 7:
        raise Exception("No related videos presented")
    try:
        only_click_video(driver, related_videos, True, search_term, do_not_click)
    except Exception as e:
        raise Exception(e)


def get_video_object(driver):
    i = 1
    while i < 7:
        try:
            WebDriverWait(driver, timeout=5).until(
                EC.visibility_of_element_located((By.ID, "movie_player"))
            )
            response = driver.execute_script(
                'return document.getElementById("movie_player")?.getPlayerResponse()'
            )
            return response
        except:
            print("no video")
            i += 1
    raise Exception("Could not get 'movie player' object")


def only_click_video(logger, driver, videos, related_click=False, search_term=None):
    if related_click == False:  # if first search and click, click a random video
        for num, index in enumerate(range(1, 6)):
            try:
                random_index_max = len(videos) - 1
                random_vid = random.randint(0, random_index_max)
                chosen_video = videos[random_vid]
                chosen_title = chosen_video.find_element(
                    By.ID, "video-title"
                )  # get video title
                title_str = chosen_title.text
                print(f"chose video: {title_str} on attempt {num}")
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

    else:  # if clicking related video, process provided video titles to click best fit TODO when we get to related vids
        chosen_video = None
        chosen_title = ""
        highest_ratio = 0
        for video in videos:
            try:  # if element is stale pass through to next one
                title = video.find_element(
                    By.ID, "video-title"
                ).text  # get video title\
                likeness = fuzz.partial_token_sort_ratio(
                    search_term, title
                )  # compare video title to original search term
                if likeness > highest_ratio and title:
                    highest_ratio = likeness
                    chosen_video = video
                    chosen_title = title
            except:
                pass
        if chosen_video == None:
            raise Exception("Error finding like video, restarting")
        else:
            print(
                "Found video with {} likeness, with the title {}".format(
                    highest_ratio, title
                )
            )

    for num, index in enumerate(range(1, 6)):  # get link of video
        try:
            link = chosen_title.get_attribute("href")
            break
        except Exception as e:
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

    if "watch" in link:  # check the link to see if it's a video
        for num, index in enumerate(range(1, 6)):
            try:  # try to click thumbnail if it is a video
                WebDriverWait(driver, timeout=5).until(
                    EC.element_to_be_clickable(chosen_title)
                )
                chosen_title.click()
                break
            except (
                Exception
            ) as e:  # re-grab title if unable to click due to possible stale element
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

        # Re-Do if video was unavailable, add to do not click list
        try:
            WebDriverWait(driver, 10).until(EC.title_contains(title_str))
            print(
                "title checked!"
            )  # TODO Find solution for watched and dont click lists
        except:
            print("title did not contain str")
            raise Exception("video likely unavailable")

    # elif (
    #    "watch" not in link and related_click == False
    # ):  # restart if it's not a video and click a different one (first click)
    #    search_for_term(driver, search_term)
    # else:  # restart if it's not a video and click a different one (related click)
    #    do_not_click = do_not_click.append(chosen_title)
    #    click_related_video(
    #        driver,
    #        search_term,
    #        do_not_click=do_not_click,
    #    )
