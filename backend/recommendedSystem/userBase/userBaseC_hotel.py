import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
from tqdm import tqdm
import matplotlib.pyplot as plt
import csv


# 1. 讀取資料
print("\n# 1. 讀取資料")
filePath = "MiTrip/data/qesData/qes_hotelData.csv"
data = pd.read_csv(filePath)

font = {"family": "DFKai-SB", "weight": "bold", "size": "13"}
plt.rc("font", **font)

# 2. 資料前處理
print("\n# 2. 資料前處理")

# 為每一位使用者加上編號
data["userID"] = data.index

# 3. 選取用戶特徵
print("\n# 3. 選取用戶特徵")

# 僅最喜歡的住宿類型
favoriteColumns = data[
    [
        "帳篷",
        "度假飯店",
        "民宿",
        "背包客棧",
        "膠囊旅館",
        "酒店",
        "青年旅館",
        "飯店"
    ]
]
df_favorite = favoriteColumns.idxmax(axis=1)
# df_favorite = df_favorite.apply(lambda x: x.replace("_fav", ""))
df_favorite = df_favorite.to_frame()
y = df_favorite
df_favorite = pd.concat([df_favorite, data["userID"]], axis=1)

# 使用者特徵
user_features = data[
    [
        "userID",
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
    ]
]


# 4. 切分訓練集和測試集
print("\n# 4. 切分訓練集和測試集")
test_size = 0.3
test_df = user_features.sample(frac=test_size, random_state=1)
train_df = user_features.drop(test_df.index)
train_df = train_df.drop(["userID"], axis=1)
print("訓練集資料筆數：", len(train_df))
print("測試集資料筆數：", len(test_df))


# 5. 基於內容的推薦
print("\n# 5. 基於內容的推薦")


def recommend_restaurants(user_id, num_recommendations):
    # 取得傳入使用者的特徵
    rec_data = test_df[test_df["userID"] == user_id]
    rec_data = rec_data.drop(["userID"], axis=1)

    # 合併使用者特徵與測試集特徵並計算相似度
    merged_df = pd.concat([train_df, rec_data], axis=0)
    merged_df = merged_df.dropna()
    similar_users = cosine_similarity(merged_df)
    user_similarity = similar_users[-1]

    # 排序相似度並取得前 num_recommendations 個使用者的索引
    top_users_indices = np.argsort(user_similarity)[-num_recommendations - 1 : -1][::-1]

    # 取得指定使用者的最喜歡的住宿地點
    restaurants_to_recommend = list(
        map(lambda user: df_favorite.iloc[user, 0], top_users_indices)
    )
    counter = Counter(restaurants_to_recommend)
    total_count = len(restaurants_to_recommend)
    probabilities = {key: value / total_count for key, value in counter.items()}
    sorted_probabilities = sorted(
        probabilities.items(), key=lambda x: x[1], reverse=True
    )
    return sorted_probabilities


# 6. 評估推薦結果-僅最喜歡的住宿類型
print("\n# 6. 評估推薦結果-僅最喜歡的住宿類型")

result = []
for top_n in tqdm(range(1, 9)):
    accuracy_list_fav = []
    for time in range(1, 13):
        total = 0
        sum = 0
        for user_id in test_df["userID"]:
            probabilities = recommend_restaurants(user_id, num_recommendations=time)
            probabilities = [x[0] for x in probabilities]
            # print(
            #     f"為使用者 {user_id} 推薦的餐廳: {probabilities[:3]}, 實際答案: {df_favorite.iloc[user_id, 0]}"
            # )
            if any(df_favorite.iloc[user_id, 0] in j for j in probabilities[:top_n]):
                sum += 1
            total += 1
        # print(f"推薦{time}個結果時的命中率: ", sum / total)
        accuracy_list_fav.append([time, sum / total])
    # print(f"top {top_n} 的結果: ", accuracy_list_fav)
    result.append([top_n, accuracy_list_fav])

# print(len(result))
# print(result)
# 7. 將結果繪製成圖表
print("\n# 7. 將結果繪製成圖表")
plt.figure(figsize=(10, 10))
for i in range(len(result)):
    plt.plot(
        [j[0] for j in result[i][1]],
        [j[1] for j in result[i][1]],
        label=f"top {result[i][0]}",
    )
plt.legend(loc="best")
# plt.yticks([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
plt.xlabel("從資料庫中尋找N個最相似的使用者")
plt.ylabel("命中率")
plt.title("top N 推薦住宿命中率")
for i in range(len(result)):
    for j in range(len(result[i][1])):
        plt.text(
            result[i][1][j][0],
            result[i][1][j][1],
            "{:.2f}".format(result[i][1][j][1]),
            fontsize=10,
        )
plt.show()

# 8. 將結果存成csv檔
print("\n# 8. 將結果存成csv檔")
with open("MiTrip/data/recommendedSystemResult/userBase/hotelResult.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["top_n", "accuracy"])
    for i in range(len(result)):
        for j in range(len(result[i][1])):
            writer.writerow([result[i][0], result[i][1][j][0], result[i][1][j][1]])
