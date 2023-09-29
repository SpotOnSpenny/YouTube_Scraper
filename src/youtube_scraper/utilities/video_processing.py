# ----- Python Standard Library -----
import os
import json
from math import trunc

# ----- External Dependencies -----
import pandas
from termcolor import colored

# ----- Look for Index -----
def find_index(logger):
    # ----- Colored Messages -----
    no_index = colored("No ad index found, creating one instead!", "magenta")
    index_found = colored("Found ad index!", "magenta")

    # ----- Script -----
    working_directory = os.getcwd()  # get current directory
    index_file_path = os.path.join(
        working_directory, "youtube_scraper/downloaded_ads/ad_index.csv"
    )  # create file path to index.csv from current directory
    try:  # try to open the index csv for ads
        dataframe = pandas.read_csv(index_file_path)  # open the index
        logger.info("Index found! Using existing csv.")
        print(index_found)
    except:  # create the index csv if one not found
        target_dir = os.path.join(working_directory, "youtube_scraper/downloaded_ads")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        logger.info("No index csv found, creating a new one.")
        dataframe = pandas.DataFrame(
            columns=[
                "Date Collected",
                "Ad ID",
                "Profile Used",
                "Found on Search",
                "Clicks Deep",
                "Ad Endpoint",
                "Found on Video",
                "Posting Channel",
                "Family Safe",
                "Downloaded",
            ]
        )
    return dataframe

# Parse obj for values
def find_values(obj, *keys):
    if isinstance(obj, dict):
        for key in keys:
            if key in obj:
                yield obj[key]
        obj = obj.values()
    elif not isinstance(obj, list):
        return
    for child in obj:
        yield from find_values(child, *keys)

# Process the video object for values we want
def process_data(response, ad_index, clicks, search_term, profile, date):
    print("processing...")
    new = 0
    duplicates = 0
    #locate the ads
    ads = list(find_values(response, "instreamVideoAdRenderer"))  # determine if an ad exists on the video
    if ads == []:  # when there are no ads, move on
        print("NO ADS")
        vid_data = list(find_values(response, "videoDetails"))
        video_specifics = vid_data[0]
        length = int(video_specifics["lengthSeconds"])
        ad_presence = False
        return ad_index, new, duplicates, length, ad_presence
    else:  # when there are ads, find data about the video they're once
        ad_presence = True
        vid_data = find_values(response, "videoDetails", "isFamilySafe")
        video_specifics, family_safe = vid_data
        length = int(video_specifics["lengthSeconds"])
        for ad in ads:
            try:
                ad_id = ad["externalVideoId"]
            except:
                continue #continue if it's not the right type of item
            if ad_index["Ad ID"].str.contains(ad_id).any(): 
                duplicates += 1
                print("duplicate")
            else:
                new += 1
                print("new")
            try:
                endpoint = ad["clickthroughEndpoint"]["urlEndpoint"]["url"]
            except:
                endpoint = "no endpoint"
            ad_metadata = [
                {
                    "Date Collected": date,
                    "Ad ID": ad_id,
                    "Profile Used": profile,
                    "Clicks Deep": clicks,
                    "Found on Search": search_term,
                    "Ad Endpoint": endpoint,
                    "Found on Video": video_specifics["title"],
                    "Posting Channel": video_specifics["author"],
                    "Family Safe": str(family_safe),
                    "Downloaded": False,
                }
            ]
            ad_metadata = pandas.DataFrame(ad_metadata)
            ad_index = pandas.concat([ad_index, ad_metadata], ignore_index=True)
        ad_index.to_csv(path_or_buf="./youtube_scraper/downloaded_ads/ad_index.csv", index=False)  # save CSV incase of error
        return ad_index, new, duplicates, length, ad_presence


def determine_ad_length(video_obj):
    # Instantiate ad time
    ads_length = 0

    # Get the ad objects from the video object
    ads = list(find_values(video_obj, "instreamVideoAdRenderer"))

    # Parse through ads for the ones we're looking for
    for ad in ads:
        try:
            url_list = ad["pings"]["impressionPings"]
        except:
            continue

        # For each URL
        for url in url_list:
            # If it's the one we're looking for with the length of the ad
            if "ad_len" in url["baseUrl"]:
                param_list = url["baseUrl"].split("&")
                # Cycle through param list and look for ad_len
                for param in param_list:
                    # If the parameter is the length of the ad
                    if "ad_len" in param:
                        ad_len = int(param.split("=")[1])
                        ads_length += ad_len
    ads_length = ads_length/1000
    return trunc(ads_length)