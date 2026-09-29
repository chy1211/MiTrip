import mysql.connector
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
try:
    import cupy as cp  # optional GPU acceleration
except ImportError:
    import numpy as cp

# MySQL 連接配置
from config import MYSQL_CONFIG as mysql_config

def getSimilarUserById(user_id, As, An, Aw, Ae):
    # 連接 MySQL 資料庫
    conn = mysql.connector.connect(**mysql_config)

    # 修改 SQL 查詢語句，選擇需要的欄位
    sql_query = "SELECT `userID`, `18 歲以下`, `18-24 歲`, `25-34 歲`, `35-44 歲`, `45-54 歲`, `55 歲以上`, `其他`, `女`, `男`, `學生`, `家管`, `工商業人員`, `自由業`, `軍/警/公/教/人員`, `醫護人員`, `days`, `budget1Day`, `budget2Day`, `budget3-4Day`, `budget5-6Day`, `budget7Day`, `其他旅遊方式`, `自助旅行`, `跟團旅行`, `都喜歡`, `一個月 ~ 三個月前`, `一周 ~ 一個月前`, `一周前或更短時間`, `三個月 ~ 六個月前`, `1 個人`, `2 個人`, `3~5 人`, `6 人以上`, `旅遊公司官方網站或實體店面`, `旅遊書籍或雜誌`, `旅遊相關網站或APP`, `朋友親戚或同事推薦`, `網路搜尋引擎`, `不用看到討厭的人`, `增長見聞、學習新技能`, `放鬆身心、紓解壓力`, `獨立探險、尋找新鮮感`, `與親友共遊、增進感情`, `體驗當地文化、風俗習慣`, `Google Maps`, `Vlog／部落格`, `其他方式`, `旅遊網站／APP`, `文化景點`, `自然景點`, `期間活動`, `休閒娛樂`, `娛樂演出` FROM `userPreferences`"
    user_data = pd.read_sql_query(sql_query, conn)
    
    ##僅最喜歡的景點類型
    favoriteColumns = user_data[
        [
            "文化景點",
            "自然景點",
            "期間活動",
            "休閒娛樂",
            "娛樂演出"
        ]
    ]
    df_favorite = favoriteColumns.idxmax(axis=1)
    df_favorite = df_favorite.to_frame()
    y = df_favorite
    df_favorite = pd.concat([df_favorite, user_data["userID"]], axis=1)

    # 使用者特徵
    user_features = user_data[
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
    # 取得傳入使用者的特徵
    target_user = user_features[user_features["userID"] == user_id]
    target_user = target_user.drop(["userID"], axis=1)

    # 將使用者的特徵與其他所有使用者的特徵計算相似度
    user_similarity = cosine_similarity(target_user, user_features.drop(["userID"], axis=1))
    user_similarity = cp.argsort(user_similarity)[0][::-1]

    # 排序相似度並取得前10%相似的使用者的索引
    num_users = int(len(user_similarity) * 0.1)
    top_users_indices = cp.argsort(user_similarity)[-num_users - 1: -1][::-1]

    # 取得相似使用者的最喜歡的景點
    favorite_attractions = list(
        map(lambda user: df_favorite.iloc[user, 0], top_users_indices)
    )
    counter = Counter(favorite_attractions)
    total_count = len(favorite_attractions)
    probabilities = {key: value / total_count for key, value in counter.items()}
    sorted_probabilities = sorted(
        probabilities.items(), key=lambda x: x[1], reverse=True
    )
    # 取得前三個景點類型
    top_three_recommendations = [key for key, _ in sorted_probabilities[:3]]
    # 相似使用者喜歡的類型不足 3 種時，重複最後一種補滿（原本會 IndexError，推薦 API 回 500）
    while top_three_recommendations and len(top_three_recommendations) < 3:
        top_three_recommendations.append(top_three_recommendations[-1])
    if not top_three_recommendations:
        conn.close()
        return []
    # 插入查詢指令，找出這些相似使用者可能喜歡的景點
    sql_query = '''
        SELECT id, class
        FROM AttractionData
        WHERE `lat` BETWEEN %s AND %s
          AND `lng` BETWEEN %s AND %s
          AND (JSON_CONTAINS(class, '["{}"]') OR JSON_CONTAINS(class, '["{}"]') OR JSON_CONTAINS(class, '["{}"]'));
    '''.format(*top_three_recommendations)

    cursor = conn.cursor()
    cursor.execute(sql_query, (As, An, Aw, Ae))
    attractions = cursor.fetchall()

    # 對景點進行排序 排序標準是根據相似使用者的個數
    def weighted_sort(attraction, top_users):
        def get_user_count(attraction_id):
            return sum(attraction_id in top_users for user in top_users)

        def custom_sort_key(item):
            attraction_id, _ = item
            user_count = get_user_count(attraction_id)
            return user_count

        sorted_attractions = sorted(attraction, key=custom_sort_key, reverse=True)
        return sorted_attractions

    sorted_attractions = weighted_sort(attractions, top_three_recommendations)
    sorted_attraction_ids = [attraction[0] for attraction in sorted_attractions]

    cursor.close()
    conn.close()
    return sorted_attraction_ids

# 推薦景點
# print(getSimilarUserById(123, 25.0, 30.0, -80.0, -70.0))
