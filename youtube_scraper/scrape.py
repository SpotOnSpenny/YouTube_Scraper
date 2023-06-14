# ----- Imports -----
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import random

# ----- Environment Setup -----
def entrypoint():
    print("----- Welcome to the M2K YouTube Ad Scraper -----\n")
    print("This program is designed to scrape a fresh YouTube window for ads based on your defined search term.\n")
    user_term = input("To begin, please enter the search term you'd like to browse for ads:\n")
    download_target = input("Next, please specify a number of ads that you would like to scrape:\n")
    driver = webdriver.Chrome()
    action = ActionChains(driver)
    get_youtube(driver)
    search_and_click(driver, user_term)
    downloaded_ads = 0
    clicks = 1
    while downloaded_ads < int(download_target):
        result = check_for_ad(driver, clicks, action)
        if result == True:
            downloaded_ads += 1
            clicks += 1
            if downloaded_ads == int(download_target):
                pass
            else:
                click_related_video(driver)
        else:
            clicks += 1
            click_related_video(driver)
    print("successfully found {} ads, exiting script.".format(download_target))
    exit()
#TODO Add error handling and logging
#TODO Add verification of user inputs

# ----- Starts WebClient and Retreives Youtube -----
def get_youtube(driver): 
    driver.get("https://youtube.com")
    print("Successfully loaded YouTube")
#TODO add error handling and logging 


# ----- Searches for Term and Selects Random Video -----
def search_and_click(driver, search_term):
    search_bar = WebDriverWait(driver, timeout=5).until(EC.element_to_be_clickable((By.NAME, "search_query")))
    print ("Search bar found, conducting search for {}".format(search_term))
    search_bar.send_keys(search_term)
    search_bar.send_keys(Keys.RETURN)
    WebDriverWait(driver, timeout=5).until(EC.title_contains(search_term))
    search_results = driver.find_elements(By.TAG_NAME, "ytd-video-renderer")
    number_of_results = len(search_results)
    random_vid = random.randint(0, number_of_results)
    print("Found {} videos on page one, clicking on video number {}".format(number_of_results, random_vid))
    search_results[random_vid].click()
    pass
#TODO add error handling and logging

def check_for_ad(driver, clicks, action):
    try:
        WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.CLASS_NAME, "ytp-ad-player-overlay")))
    except:
        print("No ad found, moving to related video #{}".format(clicks))
        return False
    else:
        print("Ad found!")
        download_ad(driver, action)
        print("Ad downloaded, moving to related video #{}".format(clicks))
        return True
#TODO Clicked a channel, gotta fix that
#TODO Add logic to download ad

def download_ad(driver, action):
    try:
        raw_id = driver.find_element(By.CLASS_NAME, "ytp-sfn-cpn").text
        ad_id = raw_id.split(" / ")[0]
    except:
        video_player = driver.find_element(By.CLASS_NAME, "ad-created") #keep an eye on this, unsure if this shows every time
        action.context_click(video_player).perform()
        context_menu = driver.find_elements(By.CLASS_NAME, "ytp-menuitem-label")
        for menu_item in context_menu:
            if menu_item.text == "Stats for nerds":
                menu_item.click()
        time.sleep(2)
        raw_id = driver.find_element(By.CLASS_NAME, "ytp-sfn-cpn").text
        ad_id = raw_id.split(" / ")[0]
    print(ad_id)

def click_related_video(driver):
    related_vids = driver.find_elements(By.CSS_SELECTOR, "ytd-compact-video-renderer.ytd-watch-next-secondary-results-renderer")
    number_of_related = len(related_vids) - 1
    random_vid = random.randint(0, number_of_related)
    video_title = related_vids[random_vid].find_element(By.ID, "video-title").text
    print("The Video title was '{}'".format(video_title))
    print("Found {} related videos on page one, clicking on video titled {}".format(number_of_related, video_title))
    related_vids[random_vid].click()
    WebDriverWait(driver, 5).until(EC.title_contains(video_title)) #don't move on until next video page loaded