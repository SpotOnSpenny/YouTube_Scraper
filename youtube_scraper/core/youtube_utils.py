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
    on_video = False
    while on_video == False:
        search_results = driver.find_elements(By.TAG_NAME, "ytd-video-renderer")
        number_of_results = len(search_results)
        random_index_max = number_of_results - 1
        random_vid = random.randint(0, random_index_max)
        search_results[random_vid].click()
        on_video = ensure_video(driver)
        if on_video == False:
            driver.back()
    pass

def click_related(driver):
    pass

def get_video_object(driver):
    WebDriverWait(driver, timeout=5).until(EC.visibility_of_element_located((By.ID, "movie_player")))
    response = driver.execute_script('return document.getElementById("movie_player")?.getPlayerResponse()')
    return response

def ensure_video(driver):
    current_url = driver.current_url
    return "watch" in current_url