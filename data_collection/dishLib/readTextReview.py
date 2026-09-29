import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd

filePath = f"{DATA_DIR}/googleMap_restaurantWithTextReviews.csv"
data = pd.read_csv(filePath)


def readFilelength():
    length = len(data)
    return length


def ifTextReviews(item):
    reviews = data["textReview"]
    if type(reviews[item]) == float:
        return False
    list = reviews[item].replace("['", "").replace("']", "").split("', '")
    for i in list:
        if i != "":
            return True
    return False


def readTextReviews(item):
    reviews = data["textReview"]
    if type(reviews[item]) == float:
        return reviews[item]
    else:
        list = reviews[item].replace("['", "").replace("']", "").split("', '")
        return list
