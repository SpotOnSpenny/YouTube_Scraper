# ----- Python Standard Library -----

# ----- External Dependencies -----
from termcolor import colored
from InquirerPy import inquirer, get_style

# ----- Internal Dependencies -----
from youtube_scraper.core.ad_processing import find_index
from youtube_scraper.core.selenium_utils import start_webdriver

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
    profile = inquirer.select(
        style = style,
        message = "Please select which demographic you'd like to check for ads with:",
        choices = ["4 YO Female", "4 YO Male - Unavailable", "6 YO Male - Unavailable", "7 YO Female - Unavailable", "9 YO Female - Unavailable", "10 YO Male - Unavailable", "No profile"]
    ).execute()
    dataframe = find_index() #find or create index for ads
    start_webdriver(profile)