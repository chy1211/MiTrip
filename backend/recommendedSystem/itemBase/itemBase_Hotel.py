import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
try:
    import cupy as cp  # optional GPU acceleration
except ImportError:
    import numpy as cp

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config


def getSimilarHotelById(hotel_ID, top_n, Rs, Rn, Rw, Re):
    # 連接到MySQL資料庫
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    try:
        # 提取飯店數據
        sql = 'SELECT id, name, rating, user_ratings_total, lowestPrice, ceilingPrice, class, numberofRooms, lat, lng FROM HotelData WHERE `lat` BETWEEN %s AND %s AND `lng` BETWEEN %s AND %s'
        val = (Rs, Rn, Rw, Re)
        cursor.execute(sql, val)
        hotels = cursor.fetchall()
        # print(f"飯店數量: {len(hotels)}")

        # 提取目標飯店數據
        sql = 'SELECT id, name, rating, user_ratings_total, lowestPrice, ceilingPrice, class, numberofRooms, lat, lng FROM HotelData WHERE `id` = %s'
        val = (hotel_ID, )
        cursor.execute(sql, val)
        target_hotel = cursor.fetchone()
        hotels.append(target_hotel)
        # print(f"目標飯店: {target_hotel[1]}")

        # 提取類別資料
        class_list = [row[6].replace('["', "").replace('"]', "").replace('"', "").split(', ') if row[6] is not None else [] for row in hotels]
        for i in range(len(hotels)):
            hotels[i] = hotels[i] + (class_list[i],)

        # 定義一個生成器函數來產生特徵
        def generate_features(hotels):
            for row in hotels:
                # 檢查類別資料是否為可迭代對象
                class_data = row[10]
                class_feature = ' '.join(class_data) if isinstance(class_data, (list, tuple)) else ''
                # print(class_feature)

                feature = f"{row[1]} {row[2]} {row[3]} {row[5]} {row[6]} {row[7]} {row[8]} {row[9]} {class_feature}"  # 使用評分、價格水平和類別作為特徵
                yield feature

        # 使用生成器函數生成特徵
        feature_generator = generate_features(hotels)

        # TF-IDF向量化，將數據類型轉換為float32
        vectorizer = TfidfVectorizer(dtype=cp.float32)
        tfidf_matrix = vectorizer.fit_transform(feature_generator)

        # 計算飯店之間的餘弦相似度，僅保留與目標飯店相似的前幾個飯店
        target_index = len(hotels) - 1
        cosine_similarities = cosine_similarity(tfidf_matrix[target_index], tfidf_matrix).flatten()

        # 根據相似度降序排序
        similar_indices = cp.argsort(cosine_similarities)[::-1]

        # 取得前10個相似的飯店索引
        top_10_similar_indices = similar_indices[1:top_n+1]  # 排除目標飯店本身

        # 將相似飯店ID存入陣列
        returnData = [hotels[index][0] for index in top_10_similar_indices]

    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
    finally:
        cursor.close()
        conn.close()
        return returnData


# print(getSimilarHotelById(4095, 100, 22.72927342284951, 22.819574321854184, 120.35042276626433, 120.44780123373567))
