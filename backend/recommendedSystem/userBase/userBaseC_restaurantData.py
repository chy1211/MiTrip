import pandas as pd
import matplotlib.pyplot as plt

# 1. 讀取資料
print("\n# 1. 讀取資料")
filePath = "MiTrip/data/qesData/qes_restaurantData.csv"
data = pd.read_csv(filePath)

font = {"family": "DFKai-SB", "weight": "bold", "size": "13"}
plt.rc("font", **font)

# 2. 資料概述
print("\n# 2. 資料概述")

# 僅最喜歡的餐廳類型
favoriteColumns = data[
    [
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
]
df_favorite = favoriteColumns.idxmax(axis=1)
df_favorite = df_favorite.apply(lambda x: x.replace("_fav", ""))

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
plt.title(f"最喜歡的餐廳類型 共{len(df_favorite)}筆資料")
plt.show()
