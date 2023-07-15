# ----- Python Standard Library -----
import time

# ----- External Dependencies -----
from termcolor import colored
from InquirerPy import inquirer, get_style

# ----- Internal Dependencies -----
from youtube_scraper.core.ad_processing import find_index, parse_json_for_ads
from youtube_scraper.core.selenium_utils import start_webdriver
from youtube_scraper.core.youtube_utils import search_for_term, get_video_object

# ----- YouTube Scraper Entrypoint -----
def entrypoint():   
    # ----- Colored Messages -----
    entry_message = colored("----- Welcome to the M2K YouTube Ad Scraper -----", "magenta", attrs=['reverse'])
    search_prompt = colored("To begin, please enter the search term you'd like to browse for ads: \n", "magenta")
    target_prompt = colored("Next, please specify a number of ads that you would like to scrape:\n", "magenta")
    invalid_error = colored("\nERROR 403:\n", "red", attrs=["bold"])
    non_digit = colored("The input you entered was invalid! Please ensure your input is a digit.\n", "red")
    invalid_digit = colored("The input you entered was invalid! Please ensure your input is greater than 0.\n", "red")
    style = get_style({"question": "#ff75b5", "questionmark": "#ff75b5", "answered_question": "#ff75b5", "answermark": "#ff75b5"})
    profiles_notice = colored("***PLEASE NOTE:*** \n due to the way that profile data works, profiles will only work on Spencer's computer \n If not on Spencer's home desktop, please select 'no profile' from the options below to run the script", "red")

    # ----- Script -----
    print(entry_message)
    search_term = input(search_prompt)
    valid_target = False
    while valid_target == False:
        download_target = input(target_prompt)
        if (download_target.isdigit()): #check that target is a number
            if (1 <= int(download_target)): #check that target is greater than 0
                download_target = int(download_target) #set target to be an integer for use later
                valid_target = True
                continue
            else:
                print(invalid_error, invalid_digit) #print error when conditions not met
        else:
            print(invalid_error, non_digit) #print error when conditions not met
    print()
    profile = inquirer.select(
        style = style,
        message = "Please select which demographic you'd like to check for ads with:",
        choices = ["4 YO Female", "4 YO Male", "6 YO Male", "7 YO Female", "9 YO Female", "10 YO Male", "No profile"]
    ).execute()
    dataframe = find_index() #find index or create new dataframe for ads
    driver = start_webdriver(profile)
    search_for_term(driver, search_term)
    video_obj = get_video_object(driver)
    print(video_obj)
    ads_on_video = parse_json_for_ads(video_obj)
    print(ads_on_video)
