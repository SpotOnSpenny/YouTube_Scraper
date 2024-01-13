# ----- Python Standard Library -----
import os

# ----- External Dependencies -----
from selenium import webdriver
from termcolor import colored
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains

# ----- Internal Dependencies -----


# ----- Start up Driver -----
class StartupError(Exception):
    def __init__(self, message):
        self.message = message


def start_webdriver(profile):
    # ----- Script -----
    options = Options()  # instantiate options
    dir_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    service = Service(executable_path=os.path.join(dir_name, "chromedriver.exe"))
    accounts_dir = r"C:\Users\Spencer\AppData\Local\Google\Chrome\User Data"  # TODO Find a way to make consistent
    options.add_argument("--user-data-dir={}".format(accounts_dir))
    match profile:  # Add profile to options depending on profile selected
        case "4F":
            options.add_argument(r"--profile-directory=Profile 4")
        case "4M":
            options.add_argument(r"--profile-directory=Profile 5")
        case "6M":
            options.add_argument(r"--profile-directory=Profile 6")
        case "7F":
            options.add_argument(r"--profile-directory=Profile 11")
        case "9F":
            options.add_argument(r"--profile-directory=Profile 2")
        case "10M":
            options.add_argument(r"--profile-directory=Profile 3")
        case "18M":
            options.add_argument(r"--profile-directory=Profile ")
        case "18F":
            options.add_argument(r"--profile-directory=Profile ")
        case _:
            options.arguments[:] = []
    options.add_argument("--mute-audio")
    try:
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Error starting chrome webdriver: {e}")
        raise StartupError(f"Error starting chrome webdriver: {e}")
    driver.get("https://youtube.com")
    action = ActionChains(driver)
    return driver, action

def check_for_driver(driver):
    try:
        driver.current_url
        return True
    except:
        return False


if __name__ == "__main__":
    start_webdriver("7F")
