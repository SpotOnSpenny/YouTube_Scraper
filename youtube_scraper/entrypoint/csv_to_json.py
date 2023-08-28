# standard python library dependencies
import pandas
import os
import datetime

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
    date = datetime.datetime.now().date()
    working_directory = os.getcwd()
    index_file_path = os.path.join(
        working_directory, "youtube_scraper/downloaded_ads/ad_index.csv"
    )
    dataframe = pandas.read_csv(index_file_path)
    dataframe.to_json("youtube_scraper/json/{}.json".format(date), orient="records")
    print(complete_message)
