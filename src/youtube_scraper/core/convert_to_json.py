# ----- Python Standard Library Imports -----
import pandas

# ----- START OF MODULE -----
def convert_to_json(file_path):
    data = pandas.read_csv(file_path)
    for index, row in data.iterrows():
        if row["Link to Video"].endswith(row["Ad ID"]):
            data.drop(index)
    data.to_json(file_path.replace(".csv", ".json"), orient="records", lines=True)

if __name__ == "__main__":
    convert_to_json("youtube_scraper/downloaded_ads/20240214_treatmentAds_4MSignedOut_YHZ.csv")
