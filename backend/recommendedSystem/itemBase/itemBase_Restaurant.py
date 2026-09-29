import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
try:
    import cupy as cp  # optional GPU acceleration
except ImportError:
    import numpy as cp

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config


def getSimilarRestaurantById(restaurant_ID, top_n, Rs, Rn, Rw, Re):
    # 連接到MySQL資料庫
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    try:
        # 提取餐廳數據
        sql = 'SELECT id, name, rating, price_level, class, serves_breakfast, serves_brunch, serves_lunch, serves_dinner, curbside_pickup, serves_beer, serves_vegetarian_food, lat, lng FROM RestaurantData WHERE `lat` BETWEEN %s AND %s AND `lng` BETWEEN %s AND %s'
        val = (Rs, Rn, Rw, Re)
        cursor.execute(sql, val)
        restaurants = cursor.fetchall()

        # 提取目標餐廳數據
        sql = 'SELECT id, name, rating, price_level, class, serves_breakfast, serves_brunch, serves_lunch, serves_dinner, curbside_pickup, serves_beer, serves_vegetarian_food, lat, lng FROM RestaurantData WHERE `id` = %s'
        val = (restaurant_ID, )
        cursor.execute(sql, val)
        target_restaurant = cursor.fetchone()
        restaurants.append(target_restaurant)
        # print(f"目標餐廳: {target_restaurant[1]}")

        # 提取類別資料
        class_list = [row[4].replace('["', "").replace('"]', "").replace('"', "").split(', ') if row[4] is not None else [] for row in restaurants]
        for i in range(len(restaurants)):
            restaurants[i] = restaurants[i] + (class_list[i],)

        # 定義一個生成器函數來產生特徵
        def generate_features(restaurants):
            for row in restaurants:
                # 檢查類別資料是否為可迭代對象
                class_data = row[14]
                class_feature = ' '.join(class_data) if isinstance(class_data, (list, tuple)) else ''

                feature = f"{row[1]} {row[2]} {row[3]} {row[5]} {row[6]} {row[7]} {row[8]} {row[9]} {row[10]} {row[11]} {row[12]} {row[13]} {class_feature}"  # 使用評分、價格水平和類別作為特徵
                yield feature

        # 使用生成器函數生成特徵
        feature_generator = generate_features(restaurants)

        # TF-IDF向量化，將數據類型轉換為float32
        vectorizer = TfidfVectorizer(dtype=cp.float32)
        tfidf_matrix = vectorizer.fit_transform(feature_generator)

        # 計算餐廳之間的餘弦相似度，僅保留與目標餐廳相似的前幾個餐廳
        target_index = len(restaurants) - 1
        cosine_similarities = cosine_similarity(tfidf_matrix[target_index], tfidf_matrix).flatten()

        # 根據相似度降序排序
        similar_indices = cp.argsort(cosine_similarities)[::-1]

        # 取得前10個相似的餐廳索引
        top_10_similar_indices = similar_indices[1:top_n+1]  # 排除目標餐廳本身

        # 打印相似的餐廳信息，包括餐廳ID
        # print(f"與ID: {restaurants[target_index][0]} -餐廳 {restaurants[target_index][1]} 相似的餐廳：")
        # for index in top_10_similar_indices:
        #     print(f"ID: {restaurants[index][0]} - 餐廳名稱: {restaurants[index][1]} - 相似度: {cosine_similarities[index]}")

        # 將相似餐廳ID存入陣列
        returnData = [restaurants[index][0] for index in top_10_similar_indices]

    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
    finally:
        cursor.close()
        conn.close()
        # print(returnData)
        return returnData
# getSimilarRestaurantById(52417, 100, 22.72927342284951, 22.819574321854184, 120.35042276626433, 120.44780123373567)
