import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd

# 1. 讀取資料
print("\n# 1. 讀取資料")
filePath = f"{DATA_DIR}/MiTrip/qes_hotelData.csv"
data = pd.read_csv(filePath)
print(data.head())

# 2. 資料處理
print("\n# 2. 資料處理")
favoriteColumns = data[["帳篷", "度假飯店", "民宿", "背包客棧", "膠囊旅館", "酒店", "青年旅館", "飯店"]]
df_favorite = favoriteColumns.idxmax(axis=1)
df_favorite = df_favorite.to_frame()

data = data.drop(
    ["帳篷", "度假飯店", "民宿", "背包客棧", "膠囊旅館", "酒店", "青年旅館", "飯店"],
    axis=1,
)

data2 = data[
    [
        "18 歲以下",
        "18-24 歲",
        "25-34 歲",
        "35-44 歲",
        "45-54 歲",
        "55 歲以上",
        "其他",
        "女",
        "男",
        "學生",
        "家管",
        "工商業人員",
        "自由業",
        "軍/警/公/教/人員",
        "醫護人員",
        "days",
        "budget1Day",
        "budget2Day",
        "budget3-4Day",
        "budget5-6Day",
        "budget7Day",
        "其他旅遊方式",
        "自助旅行",
        "跟團旅行",
        "都喜歡",
        "一個月 ~ 三個月前",
        "一周 ~ 一個月前",
        "一周前或更短時間",
        "三個月 ~ 六個月前",
        "1 個人",
        "2 個人",
        "3~5 人",
        "6 人以上",
        "旅遊公司官方網站或實體店面",
        "旅遊書籍或雜誌",
        "旅遊相關網站或APP",
        "朋友親戚或同事推薦",
        "網路搜尋引擎",
        "不用看到討厭的人",
        "增長見聞、學習新技能",
        "放鬆身心、紓解壓力",
        "獨立探險、尋找新鮮感",
        "與親友共遊、增進感情",
        "體驗當地文化、風俗習慣",
        "Google Maps",
        "Vlog／部落格",
        "其他方式",
        "旅遊網站／APP",
        "budget1DayH",
    ]
]
data = pd.concat([data2, df_favorite], axis=1)
data = data.rename(columns={0: "favorite"})
data.to_csv(
    f"{DATA_DIR}/MiTrip/qes_hotelData_fav.csv",
    index=False,
    encoding="utf-8-sig",
)
