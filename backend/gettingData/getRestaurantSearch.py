import mysql.connector
from tools.isOpening import is_opening_hours

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config


def getRestSearch(keyWord, lng, lat):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    data = None  # 初始化 data 變數
    val = None   # 初始化 val 變數
    try:
        ReturnData = {}
        sql = 'SELECT `id`, `name`, `opening_hours`, `rating`, `class`, `lat`, `lng`, `photos`, ST_DISTANCE_SPHERE(POINT(%s, %s), POINT(`lng`, `lat`)) AS distance FROM RestaurantData WHERE `name` LIKE %s ORDER BY distance'
        val = (lng, lat, '%' + keyWord + '%',)
        cursor.execute(sql, val)
        data = cursor.fetchall()

        for i in range(len(data)):
            item = list(data[i])
            if item[2]:
                ifOpening = is_opening_hours(item[2])
                if ifOpening:
                    item[2] = "營業中"
                elif ifOpening is False:
                    item[2] = "休息中"
                data[i] = tuple(item)
            if item[4]:
                item[4] = item[4].replace('["', "").replace('"]', "").replace('"', "").split(', ')
                data[i] = tuple(item)
        ReturnData[0] = {
            'id': data[0][0],
            'name': data[0][1],
            'ifOpening': data[0][2],
            'rating': data[0][3],
            'class': data[0][4],
            'lat': data[0][5],
            'lng': data[0][6],
            'photos': data[0][7]
        }

    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
    finally:
        cursor.close()
        conn.close()
        return ReturnData
