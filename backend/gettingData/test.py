import mysql.connector

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config

def getHotelSearch(keyWord, lng, lat):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(dictionary=True)  # 设置cursor为dictionary类型，返回的结果将以字典形式返回
    data = None  # 初始化 data 變數
    val = None   # 初始化 val 變數
    try:
        ReturnData = {}
        sql = 'SELECT `id`, `name`, `rating`, `class`, `lat`, `lng`, `photos`, ST_DISTANCE_SPHERE(POINT(%s, %s), POINT(`lng`, `lat`)) AS distance FROM HotelData WHERE `name` LIKE %s ORDER BY distance'
        val = (lng, lat, '%' + keyWord + '%',)
        cursor.execute(sql, val)
        data = cursor.fetchall()

        for i in range(len(data)):
            item = data[i]
            if item['class']:
                item['class'] = item['class'].replace('["', "").replace('"]', "").replace('"', "").replace('{class: ', "").replace('}', "")
            ReturnData[i] = {
                'id': item['id'],
                'name': item['name'],
                'rating': item['rating'],
                'class': item['class'],
                'lat': str(item['lat']),
                'lng': str(item['lng']),
                'photos': item['photos']
            }

    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
    finally:
        cursor.close()
        conn.close()
        return ReturnData

result = getHotelSearch('喜迎旅店', 120.399112, 22.774424)
print(result)
