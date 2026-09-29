import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

data = pd.read_csv(
    f"{DATA_DIR}/MiTrip/Mi-trip 旅遊偏好問卷 (回覆) - encoded.csv", encoding="utf-8"
)

font = {"family": "DFKai-SB", "weight": "bold", "size": "16"}
# font = {"family": "Noto-Serif-TC", "weight": "bold", "size": "16"}
plt.rc("font", **font)


# 1.您的年齡
ageColumns = [
    "18 歲以下",
    "18-24 歲",
    "25-34 歲",
    "35-44 歲",
    "45-54 歲",
    "55 歲以上",
]
ageCount = data[ageColumns].sum(axis=0)
labels = ["", "18-24 歲"] + [""] * (len(ageColumns) - 2)
plt.figure(figsize=(10, 10))
custom_colors = cm.GnBu(1 - np.arange(len(ageColumns)) / len(ageColumns))
plt.pie(ageCount, labels=labels, autopct="%1.1f%%", colors=custom_colors)
plt.axis("equal")
plt.legend(ageColumns, loc="center right", bbox_to_anchor=(1.2, 0.8), fontsize=14)
plt.tight_layout()
plt.savefig(f"{DATA_DIR}/MiTrip/pic/age.png")
plt.close()

# 2.您的性別
genderColumns = ["其他", "男", "女"]
labels = ["", "", "女"]
plt.figure(figsize=(8, 8))
genderCount = data[genderColumns].sum(axis=0)
plt.pie(
    genderCount,
    labels=labels,
    autopct="%1.1f%%",
    colors=["gray", "deepskyblue", "lightpink"],
)
plt.axis("equal")
plt.legend(genderColumns, loc="center right", bbox_to_anchor=(1.2, 0.8))
plt.tight_layout()
plt.savefig(f"{DATA_DIR}/MiTrip/pic/gender.png")
plt.close()

# 3.您的職業
jobColumns = [
    "學生",
    "家管",
    "工商業人員",
    "自由業",
    "軍/警/公/教/人員",
    "醫護人員",
]
jobCount = data[jobColumns].sum(axis=0)
labels = ["學生"] + [""] * (len(jobColumns) - 1)
plt.figure(figsize=(10, 10))
custom_colors = cm.YlOrRd(np.arange(len(jobColumns)) / len(jobColumns))
plt.pie(jobCount, labels=labels, autopct="%1.1f%%", colors=custom_colors)
plt.axis("equal")
plt.legend(jobColumns, loc="center right", bbox_to_anchor=(1.3, 0.8), fontsize=14)
plt.tight_layout()
plt.savefig(f"{DATA_DIR}/MiTrip/pic/job.png")
plt.close()

# 4.通常會花幾天在國內旅遊
data["days"] = data["days"].astype("int")
for i in range(len(data["days"])):
    if data["days"][i] == 0:
        data["days"][i] = "1 天"
    elif data["days"][i] == 1:
        data["days"][i] = "2 天"
    elif data["days"][i] == 2:
        data["days"][i] = "3-4 天"
    elif data["days"][i] == 3:
        data["days"][i] = "5-6 天"
    elif data["days"][i] == 4:
        data["days"][i] = "7 天"
    else:
        data["days"][i] = "其他"
daysCount = data["days"].value_counts().sort_index()
labels = ["", "", "3-4 天", "", ""]
plt.figure(figsize=(10, 10))
custom_colors = cm.Accent(np.arange(len(daysCount.index)) / len(daysCount.index))
plt.pie(daysCount, labels=labels, autopct="%1.1f%%", colors=custom_colors)
plt.legend(daysCount.index, loc="center right", bbox_to_anchor=(1.1, 0.9), fontsize=14)
plt.axis("equal")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/days.png")
plt.close()

# 5.通常一天的預算
data["budget1Day"] = data["budget1Day"].astype("int")
for i in range(len(data["budget1Day"])):
    if data["budget1Day"][i] == 2:
        data["budget1Day"][i] = "5,000 元以下"
    elif data["budget1Day"][i] == 3:
        data["budget1Day"][i] = "5,000-10,000 元"
    elif data["budget1Day"][i] == 0:
        data["budget1Day"][i] = "10,000-30,000 元"
    elif data["budget1Day"][i] == 1:
        data["budget1Day"][i] = "30,000 元以上"
budget1DayCount = data["budget1Day"].value_counts().sort_index()
custom_colors = cm.Accent(
    np.arange(len(budget1DayCount.index)) / len(budget1DayCount.index)
)
plt.pie(
    budget1DayCount,
    labels=budget1DayCount.index,
    autopct="%1.1f%%",
    colors=custom_colors,
)
plt.legend(
    budget1DayCount.index, loc="center right", bbox_to_anchor=(1.3, 0.8), fontsize=14
)
plt.axis("equal")
plt.title("一天的預算")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/budget1Day.png")
plt.close()

# 6.通常兩天的預算
data["budget2Day"] = data["budget2Day"].astype("int")
for i in range(len(data["budget2Day"])):
    if data["budget2Day"][i] == 2:
        data["budget2Day"][i] = "5,000 元以下"
    elif data["budget2Day"][i] == 3:
        data["budget2Day"][i] = "5,000-10,000 元"
    elif data["budget2Day"][i] == 0:
        data["budget2Day"][i] = "10,000-30,000 元"
    elif data["budget2Day"][i] == 1:
        data["budget2Day"][i] = "30,000 元以上"
budget2DayCount = data["budget2Day"].value_counts().sort_index()
custom_colors = cm.Accent(
    np.arange(len(budget2DayCount.index)) / len(budget2DayCount.index)
)
plt.pie(
    budget2DayCount,
    labels=budget2DayCount.index,
    autopct="%1.1f%%",
    colors=custom_colors,
)
plt.axis("equal")
plt.title("兩天的預算")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/budget2Day.png")
plt.close()

# 7.通常三至四天的預算
data["budget3-4Day"] = data["budget3-4Day"].astype("int")
for i in range(len(data["budget3-4Day"])):
    if data["budget3-4Day"][i] == 2:
        data["budget3-4Day"][i] = "10,000-30,000 元"
    elif data["budget3-4Day"][i] == 3:
        data["budget3-4Day"][i] = "5,000元以下"
    elif data["budget3-4Day"][i] == 0:
        data["budget3-4Day"][i] = "30,000 元以上"
    elif data["budget3-4Day"][i] == 1:
        data["budget3-4Day"][i] = "5,000-10,000 元"
budget3_4DayCount = data["budget3-4Day"].value_counts().sort_index()
print(budget3_4DayCount)
# labels = ["", "30,000 元以上", "", ""]
custom_colors = cm.Pastel2(
    np.arange(len(budget3_4DayCount.index)) / len(budget3_4DayCount.index)
)
plt.pie(budget3_4DayCount, autopct="%1.1f%%", colors=custom_colors)
plt.axis("equal")
plt.legend(
    budget3_4DayCount.index, loc="center right", bbox_to_anchor=(1.1, 0.9), fontsize=8
)
plt.close()

# 8.通常五至六天的預算
data["budget5-6Day"] = data["budget5-6Day"].astype("int")
for i in range(len(data["budget5-6Day"])):
    if data["budget5-6Day"][i] == 0:
        data["budget5-6Day"][i] = "10,000 元以下"
    elif data["budget5-6Day"][i] == 1:
        data["budget5-6Day"][i] = "10,000-30,000 元"
    elif data["budget5-6Day"][i] == 2:
        data["budget5-6Day"][i] = "30,000-50,000 元"
    elif data["budget5-6Day"][i] == 3:
        data["budget5-6Day"][i] = "50,000 元以上"
budget5_6DayCount = data["budget5-6Day"].value_counts().sort_index()
custom_colors = cm.Accent(
    np.arange(len(budget5_6DayCount.index)) / len(budget5_6DayCount.index)
)
plt.pie(
    budget5_6DayCount,
    labels=budget5_6DayCount.index,
    autopct="%1.1f%%",
    colors=custom_colors,
)
plt.axis("equal")
plt.title("五至六天的預算")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/budget5-6Day.png")
plt.close()

# 9.通常七天以上的預算
data["budget7Day"] = data["budget7Day"].astype("int")
for i in range(len(data["budget7Day"])):
    if data["budget7Day"][i] == 0:
        data["budget7Day"][i] = "10,000 元以下"
    elif data["budget7Day"][i] == 1:
        data["budget7Day"][i] = "10,000-30,000 元"
    elif data["budget7Day"][i] == 2:
        data["budget7Day"][i] = "30,000-50,000 元"
    elif data["budget7Day"][i] == 3:
        data["budget7Day"][i] = "50,000 元以上"
budget7DayCount = data["budget7Day"].value_counts().sort_index()
custom_colors = cm.Accent(
    np.arange(len(budget7DayCount.index)) / len(budget7DayCount.index)
)
plt.pie(
    budget7DayCount,
    labels=budget7DayCount.index,
    autopct="%1.1f%%",
    colors=custom_colors,
)
plt.axis("equal")
plt.title("七天以上的預算")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/budget7Day.png")
plt.close()

# 10.喜歡的旅遊方式
typeColumns = [
    "其他旅遊方式",
    "自助旅行",
    "跟團旅行",
    "都喜歡",
]
typeCount = data[typeColumns].sum().sort_values(ascending=False)
labels = ["自助旅行", "", "", ""]
custom_colors = cm.Pastel1(np.arange(len(typeCount.index)) / len(typeCount.index))
plt.pie(
    typeCount, labels=labels, autopct="%1.1f%%", colors=custom_colors, pctdistance=1.5
)
plt.legend(typeCount.index, loc="center right", bbox_to_anchor=(1.1, 0.9), fontsize=10)
plt.axis("equal")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/type.png")
plt.close()

# 11.通常會在何時進行旅遊的規劃
planTimesColumns = [
    "一個月 ~ 三個月前",
    "一周 ~ 一個月前",
    "一周前或更短時間",
    "三個月 ~ 六個月前",
]
planTimesCount = data[planTimesColumns].sum().sort_values(ascending=False)
labels = ["一個月 ~ 三個月前", "", "", ""]
custom_colors = cm.PiYG(
    1 - np.arange(len(planTimesCount.index)) / len(planTimesCount.index)
)
plt.pie(planTimesCount, labels=labels, autopct="%1.1f%%", colors=custom_colors)
plt.legend(
    planTimesCount.index, loc="center right", bbox_to_anchor=(1.1, 0.8), fontsize=8
)
plt.axis("equal")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/planTimes.png")
plt.close()

# 12.通常會與多少人一起旅遊
peopleColumns = [
    "1 個人",
    "2 個人",
    "3~5 人",
    "6 人以上",
]
peopleCount = data[peopleColumns].sum().sort_values(ascending=False)
custom_colors = cm.Accent(np.arange(len(peopleCount.index)) / len(peopleCount.index))
plt.pie(peopleCount, labels=peopleCount.index, autopct="%1.1f%%", colors=custom_colors)
plt.axis("equal")
plt.title("通常會與多少人一起旅遊")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/people.png")
plt.close()

# 14.最喜歡的旅遊主題
themeColumns = [
    "文化景點",
    "自然景點",
    "期間活動",
    "休閒娛樂",
    "娛樂演出",
]
for i in themeColumns:
    for j in range(len(data[i])):
        if data[i][j] == 5:
            data[i][j] = 1
        else:
            data[i][j] = 0
themeCount = data[themeColumns].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 10))
labels = ["自然景點", "", "", "", ""]
plt.pie(
    themeCount,
    labels=labels,
    autopct="%1.1f%%",
    colors=["palegreen", "lightskyblue", "khaki", "orange", "pink"],
)
plt.legend(themeColumns, loc="center right", bbox_to_anchor=(1.1, 1), fontsize=12)
plt.axis("equal")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/theme.png")
plt.close()

# 15.假如您要前往阿里山時，您偏好哪種交通方式呢?
transport1Columns = [
    "大眾運輸1",
    "自駕1",
]
transport1Count = data[transport1Columns].sum().sort_values(ascending=False)
custom_colors = cm.Set1(
    np.arange(len(transport1Count.index)) / len(transport1Count.index)
)
plt.pie(
    transport1Count,
    labels=transport1Count.index,
    autopct="%1.1f%%",
    colors=custom_colors,
)
plt.axis("equal")
plt.title("前往阿里山時，偏好交通方式")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/transport1.png")
plt.close()

# 16.假如您要前往市中心時，您偏好哪種交通方式呢?
transport2Columns = [
    "大眾運輸2",
    "自駕2",
]
transport2Count = data[transport2Columns].sum().sort_values(ascending=False)
custom_colors = cm.Set1(
    np.arange(len(transport2Count.index)) / len(transport2Count.index)
)
plt.pie(
    transport2Count,
    labels=transport2Count.index,
    autopct="%1.1f%%",
    colors=custom_colors,
)
plt.axis("equal")
plt.title("前往市中心時，偏好交通方式")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/transport2.png")
plt.close()

# 17. 最喜歡參加什麼樣的旅遊活動?
activityColumns = [
    "博物館、藝術展覽等文化活動",
    "戶外探險、徒步旅行、露營等冒險活動",
    "瑜珈、SPA等休閒動",
    "遊樂場、主題公園等娛樂活動",
]
activityCount = data[activityColumns].sum().sort_values(ascending=False)
custom_colors = cm.Set3(np.arange(len(activityCount.index)) / len(activityCount.index))
plt.pie(
    activityCount, labels=activityCount.index, autopct="%1.1f%%", colors=custom_colors
)
plt.axis("equal")
plt.title("最喜歡參加什麼樣的旅遊活動")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/activity.png")
plt.close()

# 18. 請問您過去旅遊時曾購買那些種類的商品呢? （多選）
goodsColumns = [
    "不太購買商品",
    # "奢侈品等高檔商品",
    "當地土產、特產",
    "當地手工藝品、文化用品等特色商品",
]
goodsCount = data[goodsColumns].sum().sort_values(ascending=False)

plt.bar(goodsCount.index, goodsCount)
plt.xticks(rotation=10)
plt.title("過去旅遊時曾購買那些種類的商品")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/goods.png")
plt.close()

# 19. 請問您通常會使用那些渠道獲取旅遊資訊呢? （多選）
infoColumns = [
    "旅遊公司官方網站或實體店面",
    "旅遊書籍或雜誌",
    "旅遊相關網站或APP",
    "朋友親戚或同事推薦",
    "網路搜尋引擎",
]
infoCount = data[infoColumns].sum().sort_values(ascending=False)

plt.bar(infoCount.index, infoCount)
plt.xticks(rotation=10)
plt.title("通常會使用那些渠道獲取旅遊資訊")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/info.png")
plt.close()

# 20. 請問您覺得在旅遊中能夠滿足那些需求? （多選）
demandColumns = [
    "不用看到討厭的人",
    "增長見聞、學習新技能",
    "放鬆身心、紓解壓力",
    "獨立探險、尋找新鮮感",
    "與親友共遊、增進感情",
    "體驗當地文化、風俗習慣",
]
demandCount = data[demandColumns].sum().sort_values(ascending=False)

plt.bar(demandCount.index, demandCount)
plt.xticks(rotation=10)
plt.title("覺得在旅遊中能夠滿足那些需求")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/demand.png")
plt.close()

# 21. 當您要出遊時會使用什麼方式去安排行程呢? （單選）
arrangeColumns = [
    "Google Maps",
    "Vlog／部落格",
    "其他方式",
    "旅遊網站／APP",
]
arrangeCount = data[arrangeColumns].sum().sort_values(ascending=False)

plt.pie(arrangeCount, labels=arrangeCount.index, autopct="%1.1f%%")
plt.axis("equal")
plt.title("當您要出遊時會使用什麼方式去安排行程呢")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/arrange.png")
plt.close()

# 22. 您喜歡在什麼樣的地方住宿呢? （多選）
stayColumns = ["帳篷", "度假飯店", "民宿", "背包客棧", "膠囊旅館", "酒店", "青年旅館", "飯店"]
stayCount = data[stayColumns].sum().sort_values(ascending=False)
custom_colors = cm.Pastel1(np.arange(len(stayColumns)) / len(stayColumns))

fig, ax = plt.subplots(figsize=(10, 6))  # 創建子圖並設置圖表尺寸
ax.bar(stayCount.index, stayCount, color=custom_colors)


# 添加百分比和次數標籤
total = stayCount.sum()
for i, v in enumerate(stayCount):
    percent = v / total * 100
    ax.text(i, v + 10, f"{percent:.1f}%", ha="center", va="bottom")
    ax.text(i, v + 10, f"({v})", ha="center", va="top")


# 調整 y 軸範圍
plt.ylim(0, max(stayCount) * 1.2)
# 調整邊緣值
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.15, top=0.9)

plt.tight_layout()
plt.savefig(f"{DATA_DIR}/MiTrip/pic/stay.png")
plt.close()
# 23. 請問您通常一晚的住宿預算為多少呢? （單選）
data["budget1DayH"] = data["budget1DayH"].astype("int")
for i in range(len(data["budget1DayH"])):
    if data["budget1DayH"][i] == 0:
        data["budget1DayH"][i] = "1000 元以下"
    elif data["budget1DayH"][i] == 1:
        data["budget1DayH"][i] = "1000-3000 元"
    elif data["budget1DayH"][i] == 2:
        data["budget1DayH"][i] = "3000-5000 元"
    elif data["budget1DayH"][i] == 3:
        data["budget1DayH"][i] = "5000-7000 元"
    elif data["budget1DayH"][i] == 4:
        data["budget1DayH"][i] = "7000元以上"
budget1DayHCount = data["budget1DayH"].value_counts().sort_values(ascending=False)
plt.figure(figsize=(10, 10))
custom_colors = cm.Pastel1(
    np.arange(len(budget1DayHCount.index)) / len(budget1DayHCount.index)
)
labels = ["1000-3000 元", "", "", "", ""]
plt.pie(budget1DayHCount, labels=labels, autopct="%1.1f%%", colors=custom_colors)
plt.legend(
    budget1DayHCount.index, loc="center right", bbox_to_anchor=(1.1, 1), fontsize=12
)
plt.axis("equal")
plt.savefig(f"{DATA_DIR}/MiTrip/pic/budget1DayH.png")
plt.close()

# 24. 請問您最喜歡以下哪個國家的料理？（單選）
restaurantFavColumns = [
    "中式料理_fav",
    "日式料理_fav",
    "法式料理_fav",
    "泰式料理_fav",
    "港式料理_fav",
    "美式料理_fav",
    "義式料理_fav",
    "越式料理_fav",
    "韓式料理_fav",
]
restaurantFavCount = data[restaurantFavColumns].sum().sort_values(ascending=False)
label_list = []
for i in restaurantFavCount.index:
    label_list.append(i.replace("_fav", ""))
plt.figure(figsize=(10, 10))
custom_colors = [
    "lightcoral",
    "lightgrey",
    "deepskyblue",
    "orange",
    "orangered",
    "royalblue",
    "lime",
    "yellow",
    "grey",
]
plt.pie(
    restaurantFavCount,
    # labels=label_list,
    autopct="%1.1f%%",
    colors=custom_colors,
    pctdistance=0.85,
)
plt.legend(label_list, loc="center right", bbox_to_anchor=(1.1, 0.9), fontsize=12)
plt.axis("equal")
plt.tight_layout()
plt.savefig(f"{DATA_DIR}/MiTrip/pic/restaurantFav.png")
# plt.show()
plt.close()

# 25. 您平常較常去哪些國家料理的餐廳用餐？ （多選）
restaurantColumns = [
    "中式料理",
    "日式料理",
    "韓式料理",
    "義式料理",
    "美式料理",
    "泰式料理",
    "港式料理",
    "越式料理",
    "法式料理",
]
restaurantCount = data[restaurantColumns].sum().sort_values(ascending=False)

custom_colors = cm.Pastel1(np.arange(len(restaurantColumns)) / len(restaurantColumns))

fig, ax = plt.subplots(figsize=(10, 6))  # 創建子圖並設置圖表尺寸
ax.bar(restaurantColumns, restaurantCount, color=custom_colors)


# 添加百分比和次數標籤
total = restaurantCount.sum()
for i, v in enumerate(restaurantCount):
    percent = v / total * 100
    ax.text(i, v + 8, f"{percent:.1f}%", ha="center", va="bottom")
    ax.text(i, v + 8, f"({v})", ha="center", va="top")


# 調整 y 軸範圍
plt.ylim(0, max(restaurantCount) * 1.2)
# 調整邊緣值
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.15, top=0.9)

plt.tight_layout()
plt.savefig(f"{DATA_DIR}/MiTrip/pic/restaurant.png")
# plt.show()
plt.close()
