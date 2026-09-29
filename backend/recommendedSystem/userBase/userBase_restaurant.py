import pandas as pd
try:
    import cupy as cp  # optional GPU acceleration
except ImportError:
    import numpy as cp
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import mysql.connector

# MySQL 連接配置
from config import MYSQL_CONFIG as mysql_config


def getSimilarUserById(user_id, Rs, Rn, Rw, Re):
    # 連接 MySQL 資料庫
    conn = mysql.connector.connect(**mysql_config)

    # 修改 SQL 查詢語句，選擇需要的欄位
    sql_query = "SELECT `userID`, `18 歲以下`, `18-24 歲`, `25-34 歲`, `35-44 歲`, `45-54 歲`, `55 歲以上`, `其他`, `女`, `男`, `學生`, `家管`, `工商業人員`, `自由業`, `軍/警/公/教/人員`, `醫護人員`, `days`, `budget1Day`, `budget2Day`, `budget3-4Day`, `budget5-6Day`, `budget7Day`, `其他旅遊方式`, `自助旅行`, `跟團旅行`, `都喜歡`, `一個月 ~ 三個月前`, `一周 ~ 一個月前`, `一周前或更短時間`, `三個月 ~ 六個月前`, `1 個人`, `2 個人`, `3~5 人`, `6 人以上`, `旅遊公司官方網站或實體店面`, `旅遊書籍或雜誌`, `旅遊相關網站或APP`, `朋友親戚或同事推薦`, `網路搜尋引擎`, `不用看到討厭的人`, `增長見聞、學習新技能`, `放鬆身心、紓解壓力`, `獨立探險、尋找新鮮感`, `與親友共遊、增進感情`, `體驗當地文化、風俗習慣`, `Google Maps`, `Vlog／部落格`, `其他方式`, `旅遊網站／APP`, `中式料理_fav`, `日式料理_fav`, `法式料理_fav`, `泰式料理_fav`, `港式料理_fav`, `美式料理_fav`, `義式料理_fav`, `越式料理_fav`, `韓式料理_fav` FROM `userPreferences`"
    data = pd.read_sql_query(sql_query, conn)

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
    df_favorite = favoriteColumns.idxmax(axis=1).str.replace("_fav", "").to_frame(name="favorite_cuisine")
    df_favorite["userID"] = data["userID"]

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
    # 取得傳入使用者的特徵
    target_user = user_features[user_features["userID"] == user_id]
    target_user = target_user.drop(["userID"], axis=1)

    # 將使用者的特徵與其他所有使用者的特徵計算相似度
    user_similarity = cosine_similarity(target_user, user_features.drop(["userID"], axis=1))
    user_similarity = cp.argsort(user_similarity)[0][::-1]

    # 排序相似度並取得前10%相似的使用者的索引
    num_users = int(len(user_similarity) * 0.1)
    # print(f"推薦相似使用者數量: {num_users}")
    top_users_indices = cp.argsort(user_similarity)[-num_users - 1: -1][::-1]

    # 取得相似使用者的最喜歡的餐廳
    restaurants_to_recommend = list(
        map(lambda user: df_favorite.iloc[user, 0], top_users_indices)
    )
    counter = Counter(restaurants_to_recommend)
    total_count = len(restaurants_to_recommend)
    probabilities = {key: value / total_count for key, value in counter.items()}
    sorted_probabilities = sorted(
        probabilities.items(), key=lambda x: x[1], reverse=True
    )
    # 取得前四個餐廳類型
    top_four_recommendations = [key.replace('料理', '') for key, _ in sorted_probabilities[:4]]
    # 相似使用者喜歡的類型不足 4 種時，重複最後一種補滿（原本會 IndexError，推薦 API 回 500）
    while top_four_recommendations and len(top_four_recommendations) < 4:
        top_four_recommendations.append(top_four_recommendations[-1])
    if not top_four_recommendations:
        conn.close()
        return []

    # 插入查詢指令
    sql_query = '''
        SELECT id, class
        FROM RestaurantData
        WHERE `lat` BETWEEN %s AND %s
          AND `lng` BETWEEN %s AND %s
          AND (JSON_CONTAINS(class, '["{}"]') OR JSON_CONTAINS(class, '["{}"]') OR JSON_CONTAINS(class, '["{}"]') OR JSON_CONTAINS(class, '["{}"]'));
    '''.format(*top_four_recommendations)

    cursor = conn.cursor()
    cursor.execute(sql_query, (Rs, Rn, Rw, Re))
    restaurants = cursor.fetchall()
    # 對餐廳進行排序 排序標準是根據兩個因素：(1) 與頂級推薦的菜式匹配的次數，(2) 根據匹配的菜式的權重加總。
    def weighted_sort(restaurant, top_recommendations):
        def get_match_count(cuisine_list):
            return sum(cuisine in top_recommendations for cuisine in cuisine_list)

        def custom_sort_key(item):
            _, cuisines_str = item
            cuisines = eval(cuisines_str)  # 将字符串表示的列表转换为实际的列表
            match_count = get_match_count(cuisines)

            # 将匹配数量乘以相应的权重进行排序
            weights = {cuisine: index + 1 for index, cuisine in enumerate(top_recommendations)}
            weighted_match_count = sum(weights[cuisine] for cuisine in cuisines if cuisine in weights)

            return (weighted_match_count, match_count)

        sorted_restaurants = sorted(restaurant, key=custom_sort_key, reverse=True)
        return sorted_restaurants
    sorted_restaurants = weighted_sort(restaurants, top_four_recommendations)
    sorted_restaurant_ids = [restaurant[0] for restaurant in sorted_restaurants]

    cursor.close()
    conn.close()
    # print(sorted_restaurant_ids)
    return sorted_restaurant_ids


# 推薦餐廳
# print(getSimilarUserById(123, 22.72927342284951, 22.819574321854184, 120.35042276626433, 120.44780123373567))
