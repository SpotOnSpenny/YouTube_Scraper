# ----- Python Standard Library -----
import random
import time
import json

# ----- External Dependencies -----
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
# ----- Internal Dependencies -----

def click_suggested(driver):
    pass

def search_for_term(driver, search_term):
    search_bar = WebDriverWait(driver, timeout=5).until(EC.element_to_be_clickable((By.NAME, "search_query")))
    search_bar.send_keys(search_term)
    search_bar.send_keys(Keys.RETURN)
    try:
        WebDriverWait(driver, timeout=5).until(EC.title_contains(search_term))
    except:
        search_for_term(driver, search_term) #recursively put in search bar if search does not direct us to results page
    back_when_not_video(driver)
    pass

def click_related_video(driver):
    related_vids = driver.find_elements(By.CSS_SELECTOR, ".ytd-watch-next-secondary-results-renderer")
    number_of_related = len(related_vids)
    print(number_of_related)
    random_index_max = number_of_related - 1 #subtract 1 for 0 indexed list
    random_vid = random.randint(0, random_index_max)
    video_title = related_vids[random_vid].find_element(By.ID, "video-title").text
    print(video_title, )
    try:
        WebDriverWait(driver, timeout=5).until(EC.element_to_be_clickable(related_vids[random_vid]))
        related_vids[random_vid].click()
    except:
        print("Could not click video at position {}, trying a different related video".format(random_vid))
        click_related_video(driver)
    WebDriverWait(driver, 5).until(EC.title_contains(video_title)) #don't move on until next video page loaded
    back_when_not_video(driver)

def get_video_object(driver):
    try:
        WebDriverWait(driver, timeout=5).until(EC.visibility_of_element_located((By.ID, "movie_player")))
        response = driver.execute_script('return document.getElementById("movie_player")?.getPlayerResponse()')
    except:
        get_video_object(driver)
    with open("sample_object.json", "w") as outfile:
        json.dump(response, outfile)
    return response

def back_when_not_video(driver):
    on_video = False
    while on_video == False:
        search_results = driver.find_elements(By.TAG_NAME, "ytd-video-renderer")
        number_of_results = len(search_results)
        random_index_max = number_of_results - 1
        random_vid = random.randint(0, random_index_max)
        search_results[random_vid].click()
        on_video = "watch" in driver.current_url
        if on_video == False:
            driver.back()
