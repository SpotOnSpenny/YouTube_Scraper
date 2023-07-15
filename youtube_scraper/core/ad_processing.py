# ----- Python Standard Library -----
import os

# ----- External Dependencies -----
import pandas
from termcolor import colored

# ----- Internal Dependencies -----

# ----- Look for Index -----
def find_index():
    # ----- Colored Messages -----
    no_index = colored("No ad index found, creating one instead!", "magenta" )
    index_found = colored("Found ad index!", "magenta")
    
    # ----- Script -----
    working_directory = os.getcwd() #get current directory
    index_file_path = os.path.join(working_directory, "downloaded_ads/ad_index.csv") #create file path to index.csv from current directory
    try: #try to open the index csv for ads
        dataframe = pandas.read_csv("./youtube_scraper/downloaded_ads/ad_index.csv") #open the index
        print(index_found) 
    except: #create the index csv if one not found
        print(no_index)
        dataframe = pandas.DataFrame(columns = ["Ad ID", "Clicks Deep", "Found on Video"])
    return dataframe

def parse_json_for_ads(json_data):
    ad_items = json_data.get("adPlacements").get("renderer").get("linearAdSequenceRenderer", "No Ad on Video").get("linearAds")
    if ad_items == "No Ad on Video":
        return ad_items
    else:
        ads = []
        for dictionary in ad_items:
            if "instreamVideoAdRenderer" in dictionary:
                ads.append(dictionary.get("instreamVideoAdRenderer").get("externalVideoID", "Error getting ID"))
    return ads