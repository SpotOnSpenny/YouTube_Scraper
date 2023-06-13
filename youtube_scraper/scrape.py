# ----- Imports -----
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# ----- Environment Setup -----
def entrypoint():
    print("----- Welcome to the M2K YouTube Ad Scraper -----\n")
    print("This program is designed to scrape a fresh YouTube window for ads based on your defined search term.\n")
    user_term = input("To begin, please enter the search term you'd like to browse for ads:\n")
    download_target = input("Next, please specify a number of ")
    driver = webdriver.Chrome()
    get_youtube(driver)
    search_and_click(driver, user_term)
    # ^ Above gets to first video, Below checks for ad, and goes to next video
    downloaded_ads = 0

    pass

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

def wait_for_ad():
    #TODO write script that checks to see if there's an ad
    pass

def download_ad():
    #TODO write script that downloads ad once on has been found
    pass