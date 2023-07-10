# ----- Python Standard Library -----

# ----- External Dependencies -----
from selenium import webdriver
from termcolor import colored

# ----- Internal Dependencies -----

# ----- Start up Driver -----
def start_webdriver(profile):
    # ----- Colored Messages -----
    profile = colored("Opening browser with profile {}".format(profile), "magenta")
    no_profile = colored ("Opening browser without associated browsing info")
    ["4 YO Female",
    "4 YO Male - Unavailable",
    "6 YO Male - Unavailable", 
    "7 YO Female - Unavailable", 
    "9 YO Female - Unavailable", 
    "10 YO Male - Unavailable", 
    "No profile"]

    # ----- Script -----
    match profile:
        case 1:
            print(profile)
        case _:
            print(no_profile)