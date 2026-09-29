import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

data = pd.read_csv(
    f"{DATA_DIR}/MiTrip/Mi-trip 旅遊偏好問卷 (回覆) - Verification.csv", encoding="utf-8"
)
encoder = OrdinalEncoder()

# 處理問卷資料
# 異常值處理
data["3.您的職業? （單選）"].replace({"保姆": "家管"}, inplace=True)
data["3.您的職業? （單選）"].replace({"保母": "家管"}, inplace=True)
data["3.您的職業? （單選）"].replace({"保育人員": "家管"}, inplace=True)
data["3.您的職業? （單選）"].replace({"幼兒保母": "家管"}, inplace=True)
data["3.您的職業? （單選）"].replace({"托育人員": "家管"}, inplace=True)
data["3.您的職業? （單選）"].replace({"旅遊業": "工商業人員"}, inplace=True)
data["3.您的職業? （單選）"].replace({"服務業": "工商業人員"}, inplace=True)
data["3.您的職業? （單選）"].replace({"社工": "醫護人員"}, inplace=True)
data["3.您的職業? （單選）"].replace({"退休": "自由業"}, inplace=True)
data["3.您的職業? （單選）"].replace({"金融業": "工商業人員"}, inplace=True)

for i in data["10. 您喜歡什麼樣的旅遊方式? （單選）"]:
    if i.startswith("國內自助"):
        data["10. 您喜歡什麼樣的旅遊方式? （單選）"].replace({f"{i}": "自助旅行"}, inplace=True)
    if i != "自助旅行" and i != "跟團旅行" and i != "都喜歡":
        data["10. 您喜歡什麼樣的旅遊方式? （單選）"].replace({f"{i}": "其他旅遊方式"}, inplace=True)

for i in data["21. 當您要出遊時會使用什麼方式去安排行程呢? （單選）"]:
    if i != "Google Maps" and i != "旅遊網站／APP" and i != "Vlog／部落格":
        data["21. 當您要出遊時會使用什麼方式去安排行程呢? （單選）"].replace({f"{i}": "其他方式"}, inplace=True)

# one-hot 值重複處理
data["15. 假如您要前往阿里山時，您偏好哪種交通方式呢?  （單選）"].replace({"自駕": "自駕1"}, inplace=True)
data["15. 假如您要前往阿里山時，您偏好哪種交通方式呢?  （單選）"].replace({"大眾運輸": "大眾運輸1"}, inplace=True)

data["16. 假如您要前往市中心時，您偏好哪種交通方式呢?  （單選）"].replace({"自駕": "自駕2"}, inplace=True)
data["16. 假如您要前往市中心時，您偏好哪種交通方式呢?  （單選）"].replace({"大眾運輸": "大眾運輸2"}, inplace=True)

data["24. 請問您最喜歡以下哪個國家的料理？（單選）"].replace({"中式料理": "中式料理_fav"}, inplace=True)
data["24. 請問您最喜歡以下哪個國家的料理？（單選）"].replace({"日式料理": "日式料理_fav"}, inplace=True)
data["24. 請問您最喜歡以下哪個國家的料理？（單選）"].replace({"法式料理": "法式料理_fav"}, inplace=True)
data["24. 請問您最喜歡以下哪個國家的料理？（單選）"].replace({"泰式料理": "泰式料理_fav"}, inplace=True)
data["24. 請問您最喜歡以下哪個國家的料理？（單選）"].replace({"港式料理": "港式料理_fav"}, inplace=True)
data["24. 請問您最喜歡以下哪個國家的料理？（單選）"].replace({"美式料理": "美式料理_fav"}, inplace=True)
data["24. 請問您最喜歡以下哪個國家的料理？（單選）"].replace({"義式料理": "義式料理_fav"}, inplace=True)
data["24. 請問您最喜歡以下哪個國家的料理？（單選）"].replace({"越式料理": "越式料理_fav"}, inplace=True)
data["24. 請問您最喜歡以下哪個國家的料理？（單選）"].replace({"韓式料理": "韓式料理_fav"}, inplace=True)

# drop 無用欄位
data = data.drop("時間戳記", axis=1)
data = data.drop("13. 請問您最喜歡什麼樣的旅遊主題?  （單選）", axis=1)

# 處理年齡並進行 one-hot encoding
# 1.您的年齡? （單選）
one_hot_age = pd.get_dummies(data["1.您的年齡? （單選）"])
data = data.drop("1.您的年齡? （單選）", axis=1)
data = data.join(one_hot_age)

# 處理性別並進行 one-hot encoding
# 2.您的心理性別? （單選）
one_hot_gender = pd.get_dummies(data["2.您的心理性別? （單選）"])
data = data.drop("2.您的心理性別? （單選）", axis=1)
data = data.join(one_hot_gender)

# 處理職業並進行 one-hot encoding
# 3.您的職業? （單選）
one_hot_job = pd.get_dummies(data["3.您的職業? （單選）"])
data = data.drop("3.您的職業? （單選）", axis=1)
data = data.join(one_hot_job)

# 處理國內旅遊天數 並進行 Ordinal Encoding
# 4.您通常會花幾天在國內旅行? （單選）
data["days"] = encoder.fit_transform(data[["4.您通常會花幾天在國內旅行? （單選）"]])
# for i in range(len(data["days"])):
#     print(data["days"][i], "->", data["4.您通常會花幾天在國內旅行? （單選）"][i])
data = data.drop("4.您通常會花幾天在國內旅行? （單選）", axis=1)

# 處理出遊1天預算 並進行 Ordinal Encoding
# 5.請問如果出遊1天您願意花費多少預算? （單選）
data["budget1Day"] = encoder.fit_transform(data[["5.請問如果出遊1天您願意花費多少預算? （單選）"]])
# for i in range(len(data["budget1Day"])):
#     print(data["budget1Day"][i], "->", data["5.請問如果出遊1天您願意花費多少預算? （單選）"][i])
data = data.drop("5.請問如果出遊1天您願意花費多少預算? （單選）", axis=1)

# 處理出遊2天預算 並進行 Ordinal Encoding
# 6. 請問如果出遊2天您願意花費多少預算? （單選）
data["budget2Day"] = encoder.fit_transform(data[["6. 請問如果出遊2天您願意花費多少預算? （單選）"]])
# for i in range(len(data["budget2Day"])):
#     print(data["budget2Day"][i], "->", data["6. 請問如果出遊2天您願意花費多少預算? （單選）"][i])
data = data.drop("6. 請問如果出遊2天您願意花費多少預算? （單選）", axis=1)

# 處理出遊3-4天預算 並進行 Ordinal Encoding
# 7. 請問如果出遊3-4天您願意花費多少預算? （單選）
data["budget3-4Day"] = encoder.fit_transform(data[["7. 請問如果出遊3-4天您願意花費多少預算? （單選）"]])
# for i in range(len(data["budget3-4Day"])):
#     print(data["budget3-4Day"][i], "->", data["7. 請問如果出遊3-4天您願意花費多少預算? （單選）"][i])
data = data.drop("7. 請問如果出遊3-4天您願意花費多少預算? （單選）", axis=1)

# 處理出遊5-6天預算 並進行 Ordinal Encoding
# 8. 請問如果出遊5-6天您願意花費多少預算? （單選）
data["budget5-6Day"] = encoder.fit_transform(data[["8. 請問如果出遊5-6天您願意花費多少預算? （單選）"]])
# for i in range(len(data["budget5-6Day"])):
#     print(data["budget5-6Day"][i], "->", data["8. 請問如果出遊5-6天您願意花費多少預算? （單選）"][i])
data = data.drop("8. 請問如果出遊5-6天您願意花費多少預算? （單選）", axis=1)

# 處理出遊7天預算 並進行 Ordinal Encoding
# 9. 請問如果出遊7天您願意花費多少預算? （單選）
data["budget7Day"] = encoder.fit_transform(data[["9. 請問如果出遊7天您願意花費多少預算? （單選）"]])
# for i in range(len(data["budget7Day"])):
#     print(data["budget7Day"][i], "->", data["9. 請問如果出遊7天您願意花費多少預算? （單選）"][i])
data = data.drop("9. 請問如果出遊7天您願意花費多少預算? （單選）", axis=1)

# 處理旅遊方式 並進行 one-hot encoding
# 10. 您喜歡什麼樣的旅遊方式? （單選）
one_hot_travel = pd.get_dummies(data["10. 您喜歡什麼樣的旅遊方式? （單選）"])
data = data.drop("10. 您喜歡什麼樣的旅遊方式? （單選）", axis=1)
data = data.join(one_hot_travel)

# 處理何時進行旅遊的規劃 並進行 one-hot encoding
# 11. 您通常會在何時進行旅遊的規劃呢? （單選）
one_hot_planT = pd.get_dummies(data["11. 您通常會在何時進行旅遊的規劃呢? （單選）"])
data = data.drop("11. 您通常會在何時進行旅遊的規劃呢? （單選）", axis=1)
data = data.join(one_hot_planT)

# 處理與多少人一起旅遊 並進行 one-hot encoding
# 12. 通常會與多少人一起旅遊呢? （單選）
one_hot_people = pd.get_dummies(data["12. 通常會與多少人一起旅遊呢? （單選）"])
data = data.drop("12. 通常會與多少人一起旅遊呢? （單選）", axis=1)
data = data.join(one_hot_people)

# 將欄位名稱縮短
data = data.rename(
    columns={
        "14. 請選出您的旅遊地點順位（5最喜歡，1最討厭） [文化景點 　    　如：歷史遺址，考古遺址，建築，美食，古蹟，工業遺址，博物館，少數民族聚居地，音樂廳，歌劇院。]": "文化景點",
        "14. 請選出您的旅遊地點順位（5最喜歡，1最討厭） [自然景點 　    　如：自然風景，海洋景色，公園，山脈，植物，動物，海岸，島嶼。]": "自然景點",
        "14. 請選出您的旅遊地點順位（5最喜歡，1最討厭） [期間活動 　  　  如：大型活動，社區活動，節慶，宗教活動，體育盛事，貿易展銷會，企業活動。]": "期間活動",
        "14. 請選出您的旅遊地點順位（5最喜歡，1最討厭） [休閒娛樂 　　    如：運動館、KTV、購物廣場(OUTlET、購物中心)]": "休閒娛樂",
        "14. 請選出您的旅遊地點順位（5最喜歡，1最討厭） [娛樂演出 　　    如：表演藝術中心(衛武營，國家音樂廳，美術館，藝術特區)]": "娛樂演出",
    }
)

# 處理旅遊地點順位 並進行 one-hot encoding
one_hot_place = pd.get_dummies(
    data[
        [
            "文化景點",
            "自然景點",
            "期間活動",
            "休閒娛樂",
            "娛樂演出",
        ]
    ]
)
data = data.drop(
    [
        "文化景點",
        "自然景點",
        "期間活動",
        "休閒娛樂",
        "娛樂演出",
    ],
    axis=1,
)
data = data.join(one_hot_place)


# 處理前往阿里山交通方式 並進行 one-hot encoding
# 15. 假如您要前往阿里山時，您偏好哪種交通方式呢?  （單選）
one_hot_Mountain = pd.get_dummies(data["15. 假如您要前往阿里山時，您偏好哪種交通方式呢?  （單選）"])
data = data.drop("15. 假如您要前往阿里山時，您偏好哪種交通方式呢?  （單選）", axis=1)
data = data.join(one_hot_Mountain)

# 處理前往市中心 並進行 one-hot encoding
# 16. 假如您要前往市中心時，您偏好哪種交通方式呢?  （單選）
one_hot_Center = pd.get_dummies(data["16. 假如您要前往市中心時，您偏好哪種交通方式呢?  （單選）"])
data = data.drop("16. 假如您要前往市中心時，您偏好哪種交通方式呢?  （單選）", axis=1)
data = data.join(one_hot_Center)

# 處理最喜歡參加旅遊活動? 並進行 one-hot encoding
# 17. 請問您最喜歡參加什麼樣的旅遊活動?  （單選）
one_hot_Activity = pd.get_dummies(data["17. 請問您最喜歡參加什麼樣的旅遊活動?  （單選）"])
data = data.drop("17. 請問您最喜歡參加什麼樣的旅遊活動?  （單選）", axis=1)
data = data.join(one_hot_Activity)

# 處理 購買那些種類的商品呢 並進行 one-hot encoding
# 18. 請問您過去旅遊時曾購買那些種類的商品呢? （多選）
ans18 = pd.DataFrame()
for i in data["18. 請問您過去旅遊時曾購買那些種類的商品呢? （多選）"]:
    list = i.split(", ")
    ans18 = ans18.append(pd.Series(list), ignore_index=True)

ans18 = ans18.stack().reset_index(level=1, drop=True).to_frame("ans18")
one_hot_buy = pd.get_dummies(ans18["ans18"]).groupby(level=0).sum()
data = data.drop("18. 請問您過去旅遊時曾購買那些種類的商品呢? （多選）", axis=1)
data = data.join(one_hot_buy)

# 處理 獲取旅遊資訊管道 並進行 one-hot encoding
# 19. 請問您通常會使用那些渠道獲取旅遊資訊呢? （多選）
ans19 = pd.DataFrame()
for i in data["19. 請問您通常會使用那些渠道獲取旅遊資訊呢? （多選）"]:
    list = i.split(", ")
    ans19 = ans19.append(pd.Series(list), ignore_index=True)

ans19 = ans19.stack().reset_index(level=1, drop=True).to_frame("ans19")
one_hot_info = pd.get_dummies(ans19["ans19"]).groupby(level=0).sum()
data = data.drop("19. 請問您通常會使用那些渠道獲取旅遊資訊呢? （多選）", axis=1)
data = data.join(one_hot_info)

# 處理 在旅遊中能夠滿足那些需求 並進行 one-hot encoding
# 20. 請問您覺得在旅遊中能夠滿足那些需求? （多選）
ans20 = pd.DataFrame()
for i in data["20. 請問您覺得在旅遊中能夠滿足那些需求? （多選）"]:
    list = i.split(", ")
    ans20 = ans20.append(pd.Series(list), ignore_index=True)

ans20 = ans20.stack().reset_index(level=1, drop=True).to_frame("ans20")
one_hot_need = pd.get_dummies(ans20["ans20"]).groupby(level=0).sum()
data = data.drop("20. 請問您覺得在旅遊中能夠滿足那些需求? （多選）", axis=1)
data = data.join(one_hot_need)

# 處理 使用行程安排方式 並進行 one-hot encoding
# 21. 當您要出遊時會使用什麼方式去安排行程呢? （單選）
one_hot_plan = pd.get_dummies(data["21. 當您要出遊時會使用什麼方式去安排行程呢? （單選）"])
data = data.drop("21. 當您要出遊時會使用什麼方式去安排行程呢? （單選）", axis=1)
data = data.join(one_hot_plan)

# 處理 住宿偏好 並進行 one-hot encoding
# 22. 您喜歡在什麼樣的地方住宿呢? （多選）
ans22 = pd.DataFrame()
for i in data["22. 您喜歡在什麼樣的地方住宿呢? （多選）"]:
    list = i.split(", ")
    ans22 = ans22.append(pd.Series(list), ignore_index=True)

ans22 = ans22.stack().reset_index(level=1, drop=True).to_frame("ans22")
one_hot_hotel = pd.get_dummies(ans22["ans22"]).groupby(level=0).sum()
data = data.drop("22. 您喜歡在什麼樣的地方住宿呢? （多選）", axis=1)
data = data.join(one_hot_hotel)

# 處理住宿預算 並進行Ordinal Encoding
# 23. 請問您通常一晚的住宿預算為多少呢? （單選）
data["budget1DayH"] = encoder.fit_transform(data[["23. 請問您通常一晚的住宿預算為多少呢? （單選）"]])
for i in range(len(data["budget1DayH"])):
    print(data["budget1DayH"][i], data["23. 請問您通常一晚的住宿預算為多少呢? （單選）"][i])
data = data.drop("23. 請問您通常一晚的住宿預算為多少呢? （單選）", axis=1)

# 處理飲食偏好 並進行 one-hot encoding
# 24. 請問您最喜歡以下哪個國家的料理？（單選）
one_hot_food = pd.get_dummies(data["24. 請問您最喜歡以下哪個國家的料理？（單選）"])
data = data.drop("24. 請問您最喜歡以下哪個國家的料理？（單選）", axis=1)
data = data.join(one_hot_food)

# 處理飲食偏好多選 並進行 one-hot encoding
# 25. 您平常較常去哪些國家料理的餐廳用餐？ （多選）
ans25 = pd.DataFrame()
for i in data["25. 您平常較常去哪些國家料理的餐廳用餐？ （多選）"]:
    list = i.split(", ")
    ans25 = ans25.append(pd.Series(list), ignore_index=True)

ans25 = ans25.stack().reset_index(level=1, drop=True).to_frame("ans25")
one_hot_food2 = pd.get_dummies(ans25["ans25"]).groupby(level=0).sum()
data = data.drop("25. 您平常較常去哪些國家料理的餐廳用餐？ （多選）", axis=1)
data = data.join(one_hot_food2)

# 輸出處理後的資料
print("輸出完畢!")
# data.to_csv(
#     f"{DATA_DIR}/MiTrip/Mi-trip 旅遊偏好問卷 (回覆) - encoded.csv",
#     encoding="utf-8-sig",
#     index=False,
# )
