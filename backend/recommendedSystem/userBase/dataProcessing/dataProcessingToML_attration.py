import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd

# 1. 讀取資料
print("\n# 1. 讀取資料")
filePath = f"{DATA_DIR}/MiTrip/qes_attractionsData.csv"
data = pd.read_csv(filePath)
print(data.head())

# 2. 資料處理
print("\n# 2. 資料處理")
favoriteColumns = data[
    [
        "文化景點",
        "自然景點",
        "期間活動",
        "休閒娛樂",
        "娛樂演出",
    ]
]
df_favorite = favoriteColumns.idxmax(axis=1)
# df_favorite = df_favorite.apply(lambda x: x.replace("_fav", ""))
df_favorite = df_favorite.to_frame()

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
        "大眾運輸1",
        "自駕1",
        "大眾運輸2",
        "自駕2",
        "博物館、藝術展覽等文化活動",
        "戶外探險、徒步旅行、露營等冒險活動",
        "瑜珈、SPA等休閒動",
        "遊樂場、主題公園等娛樂活動",
        "不太購買商品",
        "奢侈品等高檔商品",
        "當地土產、特產",
        "當地手工藝品、文化用品等特色商品",
    ]
]
data = pd.concat([data2, df_favorite], axis=1)
data = data.rename(columns={0: "favorite"})
data.to_csv(
    f"{DATA_DIR}/MiTrip/qes_attractionsData_fav.csv",
    index=False,
    encoding="utf-8-sig",
)
