# ----- Python Standard Library -----
import os
import json

# ----- External Dependencies -----
import pandas
from termcolor import colored
from pytube import YouTube

# ----- Look for Index -----
def find_index():
    # ----- Colored Messages -----
    no_index = colored("No ad index found, creating one instead!", "magenta" )
    index_found = colored("Found ad index!", "magenta")
    
    # ----- Script -----
    working_directory = os.getcwd() #get current directory
    index_file_path = os.path.join(working_directory, "youtube_scraper/downloaded_ads/ad_index.csv") #create file path to index.csv from current directory
    try: #try to open the index csv for ads
        dataframe = pandas.read_csv(index_file_path) #open the index
        print(index_found) 
    except: #create the index csv if one not found
        print(no_index)
        dataframe = pandas.DataFrame(columns = ["Ad ID", "Profile Use", "Found on Search", "Clicks Deep", "Ad Endpoint", "Found on Video", "Posting Channel", "Family Safe", "Downloaded"])
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

def process_data(response, index, clicks, search_term, profile):
    #----- Colored Messages -----
    no_ads = colored("No ads found on video #{}, processing next video".format(clicks), "magenta")
    ad_added = colored("An Ad has been found and added to the index!", "green")
    already_downloaded = colored("A duplicate ad was found, no need to download!", 'magenta')

    #----- Script -----
    new = 0
    duplicates = 0
    ads = list(find_values(response, "instreamVideoAdRenderer")) #determine if an ad exists on the video
    processed = 0
    if ads == []: #when there are no ads, move on
        print(no_ads)
        ad_present = False
        return processed, index, ad_present, new, duplicates
    else: #when there are ads, find data about the video they're on
        vid_data = find_values(response, "videoDetails", "isFamilySafe")
        ad_present = True
        video_specifics, family_safe = vid_data
        for ad in ads:
            try:
                ad_id = ad["externalVideoId"]
            except:
                with open("no externalVideoID.json", 'w') as outfile: #save json response for troubleshooting
                    json.dump(response, outfile)
                continue #next iteration
            if check_for_duplicate(ad_id) == False: #if ad hasn't been downloaded yet, download it
                download_status = download_ad(ad_id)
                new += 1
            else:
                download_status = True
                print(already_downloaded)
                duplicates += 1
            try:
                endpoint = ad["clickthroughEndpoint"]["urlEndpoint"]["url"]
            except:
                endpoint = "no endpoint"
            ad_metadata = [{
                "Ad ID": ad_id,
                "Profile Used": profile,
                "Clicks Deep": clicks,
                "Found on Search": search_term,
                "Ad Endpoint": endpoint,
                "Found on Video": video_specifics["title"],
                "Posting Channel": video_specifics["author"],
                "Family Safe": str(family_safe),
                "Downloaded": str(download_status)
            }]
            ad_metadata = pandas.DataFrame(ad_metadata)
            index = pandas.concat([index, ad_metadata], ignore_index = True)
            processed += 1
            print(ad_added)
        index.to_csv(path_or_buf="./youtube_scraper/downloaded_ads/ad_index.csv", index=False) #save CSV incase of error
        return processed, index, ad_present, new, duplicates
    
def check_for_duplicate(ad_id):
    working_directory = os.getcwd() #get current directory
    ad_path = os.path.join(working_directory, "youtube_scraper/downloaded_ads/{}.mp4".format(ad_id))
    return os.path.isfile(ad_path)

def download_ad(ad_id):
    # ----- Colored Messages -----
    download_success = colored("Ad downloaded successfully and can be found in the downloaded ads folder.", "green")
    download_failed = colored("Ad could not be downloaded, set property to false to download later", "red")

    # ----- Script -----
    ad_url = "https://youtube.ca/watch?v={}".format(ad_id)
    working_directory = os.getcwd() #get current directory
    ad_path = os.path.join(working_directory, "youtube_scraper/downloaded_ads")
    ad = YouTube(ad_url)
    try:
        ad.streams.get_highest_resolution().download(output_path=ad_path, filename="{}.mp4".format(ad_id), max_retries=3)
        print(download_success)
        return True
    except:
        print(download_failed)
        return False #return that it's not downloaded so that we can run through and download any that gave us trouble later