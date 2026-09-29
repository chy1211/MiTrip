import pandas as pd
import matplotlib.pyplot as plt

# 1. 讀取資料
print("\n# 1. 讀取資料")
filePath = "MiTrip/data/qesData/qes_attractionsData.csv"
data = pd.read_csv(filePath)

font = {"family": "DFKai-SB", "weight": "bold", "size": "13"}
plt.rc("font", **font)

# 2. 資料概述
print("\n# 2. 資料概述")

# 僅最喜歡的餐廳類型
favoriteColumns = data[
    [
        "文化景點",
        "自然景點",
        "期間活動",
        "休閒娛樂",
        "娛樂演出"
    ]
]
df_favorite = favoriteColumns.idxmax(axis=1)
# df_favorite = df_favorite.apply(lambda x: x.replace("_fav", ""))

# 印出最喜歡的餐廳類型總數比例 並繪製圓餅圖
print(df_favorite.value_counts())
plt.figure(figsize=(10, 10))
plt.pie(
    df_favorite.value_counts(),
    labels=df_favorite.value_counts().index
    + " "
    + df_favorite.value_counts().astype(str)
    + "筆",
    autopct="%1.1f%%",
)
plt.axis("equal")
plt.title(f"最喜歡的景點類型 共{len(df_favorite)}筆資料")
plt.show()
