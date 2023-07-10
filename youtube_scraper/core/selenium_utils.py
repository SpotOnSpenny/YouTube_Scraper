# ----- Python Standard Library -----
import os
import time

# ----- External Dependencies -----
from selenium import webdriver
from termcolor import colored
from selenium.webdriver.chrome.options import Options

# ----- Internal Dependencies -----

# ----- Start up Driver -----
def start_webdriver(profile):
    # ----- Colored Messages -----
    profile_statement = colored("Opening browser with profile {}".format(profile), "magenta")
    no_profile = colored ("Opening browser without associated browsing info")

    # ----- Script -----
    options = Options() #instantiate options
    dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #path to youtube_scraper folder on current machine
    accounts_dir = os.path.join(dir_name, "YouTube_Accounts") #path to YouTube account folder
    print(accounts_dir)
    options.add_argument("--user-data-dir={}".format(accounts_dir))
    match profile: #Add profile to options depending on profile selected
        case "4 YO Female":
            options.add_argument(r"--profile-directory=4YOF")
            print(profile_statement)
        case 2:
            print("unavailable")
            exit
        case 3:
            print("unavailable")
            exit
        case 4:
            print("unavailable")
            exit
        case 5:
            print("unavailable")
            exit
        case 6:
            print("unavailable")
            exit
    print(options)
    driver = webdriver.Chrome(options=options)
    time.sleep(3000)