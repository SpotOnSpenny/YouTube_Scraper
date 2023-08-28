# ----- Python Standard Library -----
import os
import time
from zipfile import ZipFile as zip

# ----- External Dependencies -----
from selenium import webdriver
from termcolor import colored
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import gdown
import chromedriver_autoinstaller

# ----- Internal Dependencies -----


# ----- Start up Driver -----
class StartupError(Exception):
    def __init__(self, message):
        self.message = message



def start_webdriver(profile):
    # ----- Colored Messages -----
    profile_statement = colored(
        "Opening browser with profile {}".format(profile), "magenta"
    )
    no_profile = colored("Opening browser without associated browsing info", "magenta")
    profiles_not_found = colored(
        "Profile data not found, installing chrome profiles...", "magenta"
    )
    profiles_found = colored("Profile data found and ready to use", "magenta")

    # ----- Script -----
    options = Options()  # instantiate options
    dir_name = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )  # path to youtube_scraper folder on current machine
    service = Service(
        executable_path=r"C:\Users\Spencer\Desktop\M2K\Code\YouTube_Scraper\youtube_scraper\chromedriver.exe"
    )
    accounts_dir = r"C:\Users\Spencer\AppData\Local\Google\Chrome\User Data"
    if (
        os.path.exists(accounts_dir) == False
    ):  # if the chrome profile data does not exist, download it
        print(profiles_not_found)
        download_profiles(dir_name)  # download and unzip
    else:
        print(profiles_found)
    options.add_argument("--user-data-dir={}".format(accounts_dir))
    match profile:  # Add profile to options depending on profile selected
        case "4 YO Female":
            options.add_argument(r"--profile-directory=Profile 3")
            print(profile_statement)
        case "4 YO Male":
            options.add_argument(r"--profile-directory=Profile 2")
            print(profile_statement)
        case "6 YO Male":
            options.add_argument(r"--profile-directory=Profile 4")
            print(profile_statement)
        case "7 YO Female":
            options.add_argument(r"--profile-directory=Profile 2")
            print(profile_statement)
        case "9 YO Female":
            options.add_argument(r"--profile-directory=Profile 2")
            print(profile_statement)
        case "10 YO Male":
            options.add_argument(r"--profile-directory=Profile 3")
            print(profile_statement)
        case _:
            options.arguments[:] = []
            print(no_profile)
    options.add_argument("--mute-audio")
    try:
        driver = webdriver.Chrome(service=service, options=options)
    except:
        raise StartupError("Error starting chrome webdriver")
    driver.get("https://youtube.com")
    return driver


# ----- Download chrome profiles, NOTE THIS ONLY WORKS FOR SPENCER'S MACHINE -----
# Unfortunately, profiles cannot be used through these means due to Google's data encryption
def download_profiles(install_dir):
    # ----- Colored Messages -----
    downloaded = colored("Profiles downloaded successfully", "magenta")
    extracted = colored("Chrome profiles extracted successfully", "magenta")

    # ----- Script -----
    # Add logic for linux vs windows machine
    windows_profiles = "1lJJJuPeDAhArzschgLX6bKKK7RhgKtEd"
    zip_output = "{}\profiles.zip".format(install_dir)
    gdown.download(id=windows_profiles, output=zip_output)
    print(downloaded)
    extract_output = "{}\chrome_profiles".format(install_dir)
    zipped_file = zip(zip_output)
    zipped_file.extractall(extract_output)
    print(extracted)
