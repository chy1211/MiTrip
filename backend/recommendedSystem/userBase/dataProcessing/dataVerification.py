import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd

data = pd.read_csv(f"{DATA_DIR}/MiTrip/Mi-trip 旅遊偏好問卷 (回覆).csv", encoding="utf-8")

# 驗證問卷是否有效
ans13 = []
ans14 = []
for i in data["13. 請問您最喜歡什麼樣的旅遊主題?  （單選）"]:
    if i.startswith("文化景點"):
        ans13.append("1")
    elif i.startswith("自然景點"):
        ans13.append("2")
    elif i.startswith("期間活動"):
        ans13.append("3")
    elif i.startswith("休閒娛樂"):
        ans13.append("4")
    elif i.startswith("娛樂演出"):
        ans13.append("5")

columns = [
    "14. 請選出您的旅遊地點順位（5最喜歡，1最討厭） [文化景點 　    　如：歷史遺址，考古遺址，建築，美食，古蹟，工業遺址，博物館，少數民族聚居地，音樂廳，歌劇院。]",
    "14. 請選出您的旅遊地點順位（5最喜歡，1最討厭） [自然景點 　    　如：自然風景，海洋景色，公園，山脈，植物，動物，海岸，島嶼。]",
    "14. 請選出您的旅遊地點順位（5最喜歡，1最討厭） [期間活動 　  　  如：大型活動，社區活動，節慶，宗教活動，體育盛事，貿易展銷會，企業活動。]",
    "14. 請選出您的旅遊地點順位（5最喜歡，1最討厭） [休閒娛樂 　　    如：運動館、KTV、購物廣場(OUTlET、購物中心)]",
    "14. 請選出您的旅遊地點順位（5最喜歡，1最討厭） [娛樂演出 　　    如：表演藝術中心(衛武營，國家音樂廳，美術館，藝術特區)]",
]
for index, row in data.iterrows():
    ans = []
    for column in columns:
        value = row[column]
        ans.append(value)
    if ans[0] == 5:
        ans14.append("1")
    elif ans[1] == 5:
        ans14.append("2")
    elif ans[2] == 5:
        ans14.append("3")
    elif ans[3] == 5:
        ans14.append("4")
    elif ans[4] == 5:
        ans14.append("5")

different_indices = [i for i in range(len(ans13)) if ans13[i] != ans14[i]]
print("問卷總數量:", len(ans13))
print("無效問卷數量:", len(different_indices))
print("有效問卷數量:", len(ans13) - len(different_indices))


# 刪除無效問卷
data = data.drop(different_indices)
data = data.reset_index(drop=True)

# 輸出驗證後的問卷
data.to_csv(
    f"{DATA_DIR}/MiTrip/Mi-trip 旅遊偏好問卷 (回覆) - Verification.csv",
    encoding="utf-8-sig",
    index=False,
)
