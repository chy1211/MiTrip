import mysql.connector
import json
import sys
from tools.isOpening import is_opening_hours

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config


def getHotelDetail(user_id, HotelsId):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    print(f"gRD使用者ID: {user_id}")
    print(f"住宿ID: {HotelsId}")

    try:
        ReturnData = {}
        sql = 'Insert into `browsingHistory` (userID, type, history) values (%s, %s, %s);'
        data = (user_id, "hotel", HotelsId)
        cursor.execute(sql, data)
        conn.commit()

        sql = 'SELECT id, name, formatted_address, description, formatted_phone_number, website, photos, lat, lng, class, numberofRooms, lowestPrice, ceilingPrice, rating, user_ratings_total, url FROM `HotelData` WHERE id = %s;'
        val = (HotelsId, )
        cursor.execute(sql, val)
        data = cursor.fetchall()

        for i in range(len(data)):
            item = list(data[i])
            if item[9]:
                item[9] = json.loads(item[9])["class"]
                item[7] = str(item[7])
                item[8] = str(item[8])
                updated_data = tuple(item)
            classlst = []
            classlst.append(updated_data[9])

            ReturnData[i] = {
                'id': updated_data[0],
                'name': updated_data[1],
                'formatted_address': updated_data[2],
                'description': updated_data[3],
                'formatted_phone_number': updated_data[4],
                'website': updated_data[5],
                'photos': updated_data[6],
                'lat': updated_data[7],
                'lng': updated_data[8],
                'class': classlst,
                'numberofRooms': updated_data[10],
                'lowestPrice': updated_data[11],
                'ceilingPrice': updated_data[12],
                'rating': updated_data[13],
                'user_ratings_total': updated_data[14],
                'url': updated_data[15],
            }
    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
        return False, f"MySQL錯誤: {err}"
    finally:
        cursor.close()
        conn.close()
    return ReturnData
