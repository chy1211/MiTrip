import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 1. 讀取資料
print("\n# 1. 讀取資料")
filePath = f"{DATA_DIR}/MiTrip/qes_hotelData_fav.csv"
data = pd.read_csv(filePath)


# 2. 資料前處理
print("\n# 2. 資料前處理")


# 3. 選取用戶特徵
print("\n# 3. 選取用戶特徵")

X = data[
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
labels = data["favorite"]
labels = LabelEncoder().fit_transform(labels)
pca = PCA(n_components=3)
reduced_features = pca.fit_transform(X)

# 繪製3D散點圖
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# 提取降維後的每個維度
x = reduced_features[:, 0]
y = reduced_features[:, 1]
z = reduced_features[:, 2]

# 繪製散點圖，按分類標籤進行著色
scatter = ax.scatter(x, y, z, c=labels)

# 添加顏色條
plt.colorbar(scatter)

# 設置標籤和標題
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_zlabel("PC3")
ax.set_title("3D Scatter Plot of Features after PCA")

# 顯示圖形
plt.show()
