import mysql.connector
import json

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config


def getHotelSearch(keyWord, lng, lat):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    data = None  # 初始化 data 變數
    val = None   # 初始化 val 變數
    try:
        ReturnData = {}
        sql = 'SELECT `id`, `name`, `rating`, `class`, `lat`, `lng`, `photos`, ST_DISTANCE_SPHERE(POINT(%s, %s), POINT(`lng`, `lat`)) AS distance FROM HotelData WHERE `name` LIKE %s ORDER BY distance'
        val = (lng, lat, '%' + keyWord + '%',)
        # print(val)
        cursor.execute(sql, val)
        data = cursor.fetchall()
        # print(data)

        for i in range(len(data)):
            item = list(data[i])
            if item[3]:
                item[3] = json.loads(item[3])["class"]
                data[i] = tuple(item)
        
        ReturnData[0] = {
            'id': data[0][0],
            'name': data[0][1],
            'rating': data[0][2],
            'class': data[0][3],
            'lat': data[0][4],
            'lng': data[0][5],
            'photos': data[0][6]
        }

    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
    finally:
        cursor.close()
        conn.close()
        return ReturnData


# print(getHotelSearch('喜迎旅店', 120.399112, 22.774424))