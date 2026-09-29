import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd
import matplotlib.pyplot as plt
import readTextReview as rTR

filePath = f"{DATA_DIR}/restaurant_output.csv"

data = pd.read_csv(filePath)
dataLength = len(data)
allDataLength = dataLength

for i in range(len(data)):
    if type(i) == float:
        dataLength -= 1
    elif rTR.ifTextReviews(i) is False:
        dataLength -= 1

NoneTextReview = allDataLength - dataLength
ifTextReview = dataLength

for i in data["class"]:
    if i == "None":
        allDataLength -= 1

ifClassified = allDataLength

font = {"family": "DFKai-SB", "weight": "bold", "size": "12"}
plt.rc("font", **font)  # pass in the font dict as kwargs
plt.rc("axes", unicode_minus=False)

labels = [
    f"有分類\n{ifClassified}筆",
    f"沒有評論\n{NoneTextReview}筆",
    f"有評論但沒分類\n{ifTextReview - ifClassified}筆",
]
sizes = [ifClassified, NoneTextReview, ifTextReview - ifClassified]
explode = (0, 0, 0.1)
plt.pie(
    sizes,
    explode=explode,
    labels=labels,
    autopct="%1.1f%%",
    shadow=False,
    startangle=90,
)
plt.title(f"餐廳評論分類結果 共{len(data)}筆資料 2023/03/12")
plt.axis("equal")
plt.show()
