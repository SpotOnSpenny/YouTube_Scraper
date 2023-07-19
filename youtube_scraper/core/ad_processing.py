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
        dataframe = pandas.DataFrame(columns = ["Ad ID", "Clicks Deep", "Ad_Endpoint", "Found on Video", "Posting Channel", "Video Tags", "Family Safe"])
    return dataframe

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

def process_data(response, index, clicks):
    #----- Colored Messages -----
    no_ads = colored("No ads found on video, processing next video", "magenta")
    ad_added = colored("An Ad has been found and added to the index!", "magenta")

    #----- Script -----
    ads = list(find_values(response, "instreamVideoAdRenderer")) #determine if an ad exists on the video
    processed = 0
    if ads == []: #when there are no ads, move on
        print(no_ads)
        return processed, index
    else: #when there are ads, find data about the video they're on
        vid_data = find_values(response, "videoDetails", "isFamilySafe")
        video_specifics, family_safe = vid_data
        for ad in ads:
            ad_metadata = [{
                "Ad ID": ad["externalVideoId"],
                "Clicks Deep": clicks,
                "Ad Endpoint": ad["clickthroughEndpoint"]["urlEndpoint"]["url"],
                "Found on Video": video_specifics["title"],
                "Posting Channel": video_specifics["author"],
                "Family Safe": family_safe
            }]
            ad_metadata = pandas.DataFrame(ad_metadata)
            index = pandas.concat([index, ad_metadata], ignore_index = True)
            processed += 1
        index.to_csv(path_or_buf="./youtube_scraper/downloaded_ads/index.csv", index=False) #save CSV incase of error
        print(ad_added)
        return processed, index