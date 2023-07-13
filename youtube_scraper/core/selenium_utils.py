# ----- Python Standard Library -----
import os
import time
from zipfile import ZipFile as zip

# ----- External Dependencies -----
from selenium import webdriver
from termcolor import colored
from selenium.webdriver.chrome.options import Options
import gdown

# ----- Internal Dependencies -----

# ----- Start up Driver -----
def start_webdriver(profile):
    # ----- Colored Messages -----
    profile_statement = colored("Opening browser with profile {}".format(profile), "magenta")
    no_profile = colored("Opening browser without associated browsing info", "magenta")
    profiles_not_found = colored("Profile data not found, installing chrome profiles...", "magenta")
    profiles_found = colored("Profile data found and ready to use", "magenta")

    # ----- Script -----
    options = Options() #instantiate options
    dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #path to youtube_scraper folder on current machine
    accounts_dir = dir_name + r"\chrome_profiles"
    if os.path.exists(accounts_dir) == False: #if the chrome profile data does not exist, download it
        print(profiles_not_found)
        zip_file = download_profiles(dir_name) #download and unzip
    else:
        print(profiles_found)
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
        case _:
            options = None
            print(no_profile)
    print(options)
    driver = webdriver.Chrome(options=options)
    driver.get("https://youtube.com")
    return driver

def download_profiles(install_dir):
    # ----- Colored Messages -----
    downloaded = colored("Profiles downloaded successfully", "magenta")
    extracted = colored("Chrome profiles extracted successfully", "magenta")

    # ----- Script -----
    #Add logic for linux vs windows machine
    windows_profiles = "1lJJJuPeDAhArzschgLX6bKKK7RhgKtEd"
    zip_output = "{}\profiles.zip".format(install_dir)
    gdown.download(id=windows_profiles, output=zip_output)
    print(downloaded)
    extract_output = "{}\chrome_profiles".format(install_dir)
    zipped_file = zip(zip_output)
    print(zipped_file)
    zipped_file.extractall(extract_output)
    print(extracted)
    return zip_output