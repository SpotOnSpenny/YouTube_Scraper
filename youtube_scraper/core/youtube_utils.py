# ----- Python Standard Library -----
import random

# ----- External Dependencies -----
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from thefuzz import fuzz

def click_suggested(driver):
    pass

def search_for_term(driver, search_term):
    search_bar = WebDriverWait(driver, timeout=5).until(EC.element_to_be_clickable((By.NAME, "search_query")))
    search_bar.send_keys(search_term)
    search_bar.send_keys(Keys.RETURN)
    try:
        WebDriverWait(driver, timeout=5).until(EC.title_contains(search_term))
    except:
        search_bar.clear()
        search_for_term(driver, search_term) #recursively put in search bar if search does not direct us to results page
    search_results = driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer.ytd-item-section-renderer")
    only_click_video(driver, search_results, False)
    pass

def click_related_video(driver, search_term):
    #get related videos
    try:
        WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div#above-the-fold"))) #wait for vid to load
        related_videos = []
        while len(related_videos) < 10:#wait for all related video items to render
            related_videos = driver.find_elements(By.TAG_NAME, "ytd-compact-video-renderer") #find all related video elements now that they've rendered
    except:
        click_related_video(driver, search_term)
    try:
        only_click_video(driver, related_videos, True, search_term)
    except Exception as e:
        raise Exception(e)
    pass

def get_video_object(driver):
    try:
        WebDriverWait(driver, timeout=5).until(EC.visibility_of_element_located((By.ID, "movie_player")))
        response = driver.execute_script('return document.getElementById("movie_player")?.getPlayerResponse()')
    except:
        get_video_object(driver)
    return response

def only_click_video(driver, videos, related_click, search_term=None):
    if related_click == False: #if first search and click, click a random video
        random_index_max = len(videos) - 1
        random_vid = random.randint(0, random_index_max)
        chosen_video = videos[random_vid]
    else: #if clicking related video, process provided video titles to click best fit
        chosen_video = None
        highest_ratio = 0
        for video in videos:
            title = video.find_element(By.ID, "video-title").text #get video title
            likeness = fuzz.partial_token_sort_ratio(search_term, title) #compare video title to original search term
            if likeness > highest_ratio:
                highest_ratio = likeness
                chosen_video = video
        print("Found video with {} likeness, with the title {}".format(highest_ratio, title))
        if chosen_video == None:
            raise Exception("Error finding like video, restarting")
    try: #try to find thumbnail of random video of those passed in
        video_thumbnail = chosen_video.find_element(By.TAG_NAME, "ytd-thumbnail")
        WebDriverWait(driver, timeout=5).until(EC.visibility_of(video_thumbnail))
        link = video_thumbnail.find_element(By.CSS_SELECTOR, "a#thumbnail").get_attribute("href")
    except: #retry if cannot locate element
        only_click_video(driver, videos, related_click, search_term)
    if "watch" in link: #check the link to see if it's a video
        try: #try to click thumbnail if it is a video
            WebDriverWait(driver, timeout= 5).until(EC.element_to_be_clickable(video_thumbnail))
            video_thumbnail.click()
        except: #retry if unable to click
            only_click_video(driver, videos, related_click, search_term)
    else: #restart if it's not a video  and click a different one
        only_click_video(driver, videos, related_click, search_term)
