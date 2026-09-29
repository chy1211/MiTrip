import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import googlemaps
from datetime import datetime
import time
import pandas as pd
import json

gmaps = googlemaps.Client(key=os.environ["GOOGLE_MAPS_API_KEY"])


def get_cities():
    filePath = (
        "C:/Users/henry/Documents/GitHub/PythonLearning/GraduationProject/VOTROC.json"
    )
    json_data = open(filePath, "r", encoding="utf-8")
    # 讀取json檔案
    data = json.load(json_data)
    # 以列表形式回傳所有縣市
    return list(data.keys())


def get_sector(city):
    filePath = (
        "C:/Users/henry/Documents/GitHub/PythonLearning/GraduationProject/VOTROC.json"
    )
    json_data = open(filePath, "r", encoding="utf-8")
    # 讀取json檔案
    data = json.load(json_data)
    temp = []
    for i in range(0, len(data[city])):
        sec = str(data[city][i].keys()).replace("dict_keys(['", "").replace("'])", "")
        temp.append(sec)
    return temp  # 回傳區域列表


def get_area_list(city, sector):
    filePath = (
        "C:/Users/henry/Documents/GitHub/PythonLearning/GraduationProject/VOTROC.json"
    )
    json_data = open(filePath, "r", encoding="utf-8")
    # 讀取json檔案
    data = json.load(json_data)
    temp = []
    for i in range(0, len(data[city])):
        if sector == str(data[city][i].keys()).replace("dict_keys(['", "").replace(
            "'])", ""
        ):
            for j in range(0, len(data[city][i][sector])):
                temp.append(data[city][i][sector][j])
    return temp  # 回傳區域列表


def getErrList():
    with open("errLog.txt", "r", encoding="utf-8") as f:
        errList = f.readlines()
        for i in errList:
            print(i)
        f.close()
        print(type(errList))
    return errList


def errLog(text):
    with open("errLog2.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
        f.close()


if __name__ == "__main__":
    errList = getErrList()
    ids = []
    times = 1
    for i in errList:
        i = i.replace("\n", "")
        results = []
        try:
            # Geocoding an address
            geocode_result = gmaps.geocode(i)
            loc = geocode_result[0]["geometry"]["location"]
            query_result = gmaps.places_nearby(keyword="餐廳", location=loc, radius=1000)
            results.extend(query_result["results"])
            while query_result.get("next_page_token"):
                time.sleep(2)
                query_result = gmaps.places_nearby(
                    page_token=query_result["next_page_token"]
                )
                results.extend(query_result["results"])
            print(
                f"{times}  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {i}  已成功爬取{len(results)}筆資料"
            )
            for place in results:
                ids.append(place["place_id"])
            stores_info = []  # 儲存所有店家資訊
            ids = list(set(ids))  # 去除重複id
            for id in ids:
                stores_info.append(
                    gmaps.place(place_id=id, language="zh-TW")["result"]
                )  # 取得店家資訊
            results = pd.DataFrame.from_dict(stores_info)  # 轉成dataframe
            results.to_csv(
                f"{DATA_DIR}/result/googlemap_restaurant_{i}.csv", index=False,
            )
            times += 1
            ids = []
        except Exception as e:
            print(e)
            print(f"{i} 發生錯誤")
            errLog(f"{e}{i}")
            continue
