import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd

filePath = f"{DATA_DIR}/googleMap_restaurantWithTextReviews.csv"

data = pd.read_csv(filePath, encoding="utf-8-sig")
print(data.shape)
print(data.columns)
print(data.head(5))

# data overview

#

