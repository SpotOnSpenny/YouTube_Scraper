# standard python library dependencies
import pandas

# external dependencies
from termcolor import colored


def entrypoint():
    start_message = colored(
        "Converting the ad_index csv file to json format...", "magenta"
    )
    complete_message = colored(
        "All done! You can find the json file in the /json directory", "green"
    )

    print(start_message)
    dataframe = pandas.read_csv("youtube_scraper/downloaded_ads/ad_index.csv")
    dataframe.to_json("youtube_scraper/json/ads.json", orient="records")
    print(complete_message)
