# ----- Imports -----
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import random
import pandas
from pytube import YouTube

# ----- CLI Entrypoint -----
def entrypoint():
    print("----- Welcome to the M2K YouTube Ad Scraper -----\n")
    print("Current Version: With Multi-ad Scrape")
    print("This program is designed to scrape a fresh YouTube window for ads based on your defined search term.\n")
    user_term = input("To begin, please enter the search term you'd like to browse for ads:\n")
    download_target = input("Next, please specify a number of ads that you would like to scrape:\n")
    try: #try to open the index csv for ads
        index = pandas.read_csv("./youtube_scraper/downloaded_ads/index.csv") #open the index
    except: #create the index csv if one not found
        print("No ad index found, creating one instead!")
        index = pandas.DataFrame(columns = ["Ad ID", "Clicks Deep", "Found on Video"])
    driver = webdriver.Chrome() #start the web browser
    action = ActionChains(driver) #start the action driver
    get_youtube(driver) #get youtube
    search_and_click(driver, user_term) #search based on selected input
    downloaded_ads = 0  #Ads downloaded counter
    clicks = 1 #Videos clicked counter
    while downloaded_ads < int(download_target): #Loop until downloaded ads counter matches target
        result = check_for_ad(driver, clicks) #Check for ad on video
        if result == 1: #if 1 ad found...
            index, downloaded_ads = download_ad(driver, action, clicks, index, downloaded_ads) #download it, add to index df
            downloaded_ads += 1 #increase counters
            clicks += 1
            if downloaded_ads == int(download_target): #don't click another ad if counter matches
                pass
            else:
                click_related_video(driver) #if more ads needed, look for more
        elif result > 1: #if more than one ad found
            index, downloaded_ads = multi_ad(driver, action, index, result, downloaded_ads, download_target, clicks)
            clicks += 1
            if downloaded_ads == int(download_target): #don't click another ad if counter matches
                pass
            else:
                click_related_video(driver) #if more ads needed, look for more
        else: #if no ad found
            clicks += 1 #increase click counter
            click_related_video(driver) #click the next video
    index.to_csv(path_or_buf="./youtube_scraper/downloaded_ads/index.csv", index=False)
    print("successfully found {} ads and added them to index csv, exiting script.".format(download_target))
    exit()

# ----- Retreives Youtube -----
def get_youtube(driver):
    driver.get("https://youtube.com")
    print("Successfully loaded YouTube")

# ----- Searches for Term and Selects Random Video -----
def search_and_click(driver, search_term):
    search_bar = WebDriverWait(driver, timeout=5).until(EC.element_to_be_clickable((By.NAME, "search_query")))
    print ("Search bar found, conducting search for {}".format(search_term))
    search_bar.send_keys(search_term)
    search_bar.send_keys(Keys.RETURN)
    WebDriverWait(driver, timeout=5).until(EC.title_contains(search_term))
    search_results = driver.find_elements(By.TAG_NAME, "ytd-video-renderer")
    number_of_results = len(search_results)
    random_index_max = number_of_results - 1
    random_vid = random.randint(0, random_index_max)
    print("Found {} videos on page one, clicking on video number {}".format(number_of_results, random_vid))
    search_results[random_vid].click()
    pass

# ----- Checks Current Video for Pre-Roll Ad -----
def check_for_ad(driver, clicks):
    try: #Try to find an ad
        WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.CLASS_NAME, "ytp-ad-player-overlay")))
    except:
        print("No ad found, moving to related video #{}".format(clicks))
        return 0
    try: #Try to find multiple ads
        number_of_ads = driver.find_element(By.CLASS_NAME, "ytp-ad-simple-ad-badge").text.split()
    except: #Except may not be needed, need to see what 1 ad looks like
        print("Error in finding number of ads, moving on")
    try: #try to find multiples
        ads_served = int(number_of_ads[3])
    except: #no multiples found, index error because text is just [ads, -]
        return 1
    else: #multiples found
        return ads_served

# ----- Download a Pre-roll Ad -----
def download_ad(driver, action, clicks, dataframe, downloaded):
    try: #Look to see if it can find the ID without any extra steps
        raw_id = driver.find_element(By.CLASS_NAME, "ytp-sfn-cpn").text
        ad_id = raw_id.split(" / ")[0]
    except: #If unable to locate, open "Stats for nerds" so that ad info exists on the page
        video_player = driver.find_element(By.CLASS_NAME, "ad-created")
        action.context_click(video_player).perform()
        context_menu = driver.find_elements(By.CLASS_NAME, "ytp-menuitem-label")
        for menu_item in context_menu:
            if menu_item.text == "Stats for nerds":
                menu_item.click()
        time.sleep(2)
        raw_id = driver.find_element(By.CLASS_NAME, "ytp-sfn-cpn").text
        ad_id = raw_id.split(" / ")[0]
    ad_url = "https://youtube.ca/watch?v={}".format(ad_id)
    ad = YouTube(ad_url)
    ad_metadata = [{
        "Ad ID": ad_id,
        "Clicks Deep": clicks,
        "Found on Video": driver.current_url
    }]
    ad_metadata = pandas.DataFrame(ad_metadata)
    try:
        ad.streams.get_highest_resolution().download(output_path="./youtube_scraper/downloaded_ads", filename="{}.mp4".format(ad_id), max_retries=3)
        print("ad successfully downloaded!")
    except:
        print("an error occured downloading this ad, the ad URL was '{}'".format(ad_url))
        return dataframe, downloaded
    else:
        index = pandas.concat([dataframe, ad_metadata], ignore_index = True)
        downloaded += 1
        return index, downloaded

# ----- Check Ad Length -----
def check_length(driver):
    ad_length = int(driver.find_element(By.CLASS_NAME, "ytp-ad-duration-remaining").text.split(":")[0])
    if ad_length > 0:
        return "No Wait"
    else:
        return "Wait"

# ------ Download Multiple Ads -----
def multi_ad(driver, action, dataframe, ads_served, downloaded, target, clicks):
    current_ad = int(driver.find_element(By.CLASS_NAME, "ytp-ad-simple-ad-badge").text.split()[1])
    while ads_served >= current_ad:
        should_we_wait = check_length(driver)
        if should_we_wait == "No Wait":
            dataframe, downloaded = download_ad(driver, action, clicks, dataframe, downloaded)
            print("1 ad downloaded, too long to wait for next ad")
            return dataframe, downloaded
        else:
            dataframe, downloaded = download_ad(driver, action, clicks, dataframe, downloaded)
            if downloaded == int(target): #check if download target hit and exit
                return dataframe, downloaded
            elif current_ad == ads_served: #check if current ad is the last one
                print("All ads on video downloaded! Moving on...")
                return dataframe, downloaded
            else: #if target not hit, and more ads on video, wait for next ad and restart loop
                current_ad += 1
                next_ad_text = "Ad {} of {}".format(str(current_ad), str(ads_served))
                print("downloaded 1 ad, waiting for next ad")
                WebDriverWait(driver, 65).until(EC.text_to_be_present_in_element((By.CLASS_NAME,"ytp-ad-simple-ad-badge"), next_ad_text))

#----- Click Random Related Video from Sidebar -----
def click_related_video(driver):
    related_vids = driver.find_elements(By.CSS_SELECTOR, "ytd-compact-video-renderer.ytd-watch-next-secondary-results-renderer")
    number_of_related = len(related_vids)
    random_index_max = number_of_related - 1 #subtract 1 for 0 indexed list
    random_vid = random.randint(0, random_index_max)
    video_title = related_vids[random_vid].find_element(By.ID, "video-title").text
    print("The Video title was '{}'".format(video_title))
    print("Found {} related videos on page one, clicking on video titled {}".format(number_of_related, video_title))
    try:
        related_vids[random_vid].click()
    except:
        print("Could not click video at position {}, trying a different related video".format(random_vid))
        click_related_video(driver)
    WebDriverWait(driver, 5).until(EC.title_contains(video_title)) #don't move on until next video page loaded