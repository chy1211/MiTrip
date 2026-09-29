import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
try:
    import cupy as cp  # optional GPU acceleration
except ImportError:
    import numpy as cp

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config

def getSimilarAttractionById(attraction_ID, top_n, As, An, Aw, Ae):
    # 連接到MySQL資料庫
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    try:
        # 提取景點數據
        sql = 'SELECT id, name, rating, class, lat, lng FROM AttractionData WHERE `lat` BETWEEN %s AND %s AND `lng` BETWEEN %s AND %s'
        val = (As, An, Aw, Ae)
        cursor.execute(sql, val)
        attractions = cursor.fetchall()

        # 提取目標景點數據
        sql = 'SELECT id, name, rating, class, lat, lng FROM AttractionData WHERE `id` = %s'
        val = (attraction_ID, )
        cursor.execute(sql, val)
        target_attraction = cursor.fetchone()
        attractions.append(target_attraction)

        # 定義一個生成器函數來產生特徵
        def generate_features(attractions):
            for row in attractions:
                feature = f"{row[1]} {row[2]} {row[3]}"  # 使用評分和類別作為特徵
                yield feature

        # 使用生成器函數生成特徵
        feature_generator = generate_features(attractions)

        # TF-IDF向量化，將數據類型轉換為float32
        vectorizer = TfidfVectorizer(dtype=cp.float32)
        tfidf_matrix = vectorizer.fit_transform(feature_generator)

        # 計算景點之間的餘弦相似度，僅保留與目標景點相似的前幾個景點
        target_index = len(attractions) - 1
        cosine_similarities = cosine_similarity(tfidf_matrix[target_index], tfidf_matrix).flatten()

        # 根據相似度降序排序
        similar_indices = cp.argsort(cosine_similarities)[::-1]

        # 取得前10個相似的景點索引
        top_10_similar_indices = similar_indices[1:top_n+1]  # 排除目標景點本身

        # 打印相似的景點信息，包括景點ID
        # print(f"與ID: {attractions[target_index][0]} -景點 {attractions[target_index][1]} 相似的景點：")
        # for index in top_10_similar_indices:
        #     print(f"ID: {attractions[index][0]} - 景點名稱: {attractions[index][1]} - 相似度: {cosine_similarities[index]}")

        # 將相似景點ID存入陣列
        returnData = [attractions[index][0] for index in top_10_similar_indices]

    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
    finally:
        cursor.close()
        conn.close()
        # print(returnData)
        return returnData

# getSimilarAttractionById(12345, 10, 25.0, 30.0, -80.0, -70.0)  # 請替換成實際的經緯度範圍
