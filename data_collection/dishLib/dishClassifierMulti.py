import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import jieba
import readTextReview as rTR
import dishLib as dL
import time

start_time = time.time()
print("Start reading data...")
filePath = f"{DATA_DIR}/googleMap_restaurantWithTextReviews.csv"
data = pd.read_csv(filePath)
print("Start reading dishLibrary...")
dish_library = dL.dish_lib()
fileLength = rTR.readFilelength()
print("File length: ", fileLength)
print("initializing data...")
data["class"] = "None"
print("initializing dict...")
jieba.load_userdict(f"{DATA_DIR}/dishLibrary.txt")
print("Start processing data...")


def readAndCut(i):
    text = rTR.readTextReviews(i)
    if type(text) == float:
        return "No reviews"
    else:
        seg_list = []
        for t in text:
            seg = jieba.cut(t, cut_all=False)
            seg_list.append(seg)
        return seg_list


def process_text(i):
    seg_list = readAndCut(i)
    if seg_list != "No reviews":
        type_count = {}
        for seg in seg_list:
            for word in seg:
                for cuisine, dishes in dish_library.items():
                    if word in dishes:
                        if cuisine not in type_count:
                            type_count[cuisine] = 0
                        type_count[cuisine] += 1
            sorted_types = sorted(type_count.items(), key=lambda x: x[1], reverse=True)
            sorted_List = []
            if sorted_types:
                for x in sorted_types:
                    sorted_List.append(x[0])
                data.loc[i, "class"] = str(sorted_List)


with ThreadPoolExecutor() as executor:
    executor.map(process_text, range(fileLength))
print("Start exporting data...")
data.to_csv(
    f"{DATA_DIR}/restaurant_output.csv", encoding="utf-8-sig", index=False
)
print("Done!")
print(
    "cost time: ", time.strftime("%H:%M:%S", time.localtime(time.time() - start_time))
)
