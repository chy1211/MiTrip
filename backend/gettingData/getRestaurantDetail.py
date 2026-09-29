import mysql.connector
import json
import sys
from tools.isOpening import is_opening_hours

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config


def getRestDetail(user_id, restaurantsId):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    print(f"gRD使用者ID: {user_id}")
    print(f"gRD餐廳ID: {restaurantsId}")
    try:
        ReturnData = {}
        sql = 'Insert into `browsingHistory` (userID, type, history) values (%s, %s, %s);'
        data = (user_id, "restaurant", restaurantsId)
        cursor.execute(sql, data)
        conn.commit()

        sql = 'SELECT id, formatted_address, formatted_phone_number, name, opening_hours, url, rating, wheelchair_accessible_entrance, user_ratings_total, class, photos, lat, lng, website FROM `RestaurantData` WHERE id = %s;'
        val = (restaurantsId, )
        cursor.execute(sql, val)
        data = cursor.fetchall()
        for i in range(len(data)):
            item = list(data[i])  # Convert the tuple to a list
            if item[4]:  # Check if opening hours are provided
                ifOpening = is_opening_hours(item[4])
                if ifOpening:
                    text = "營業中"
                elif ifOpening is False:
                    text = "休息中"
                item.append(text)
            updated_data = tuple(item)
            if item[4]:
                item[4] = json.loads(item[4])
                weekday_text = item[4]["weekday_text"]
                item[4] = weekday_text
                updated_data = tuple(item)
            if item[9]:
                item[9] = item[9].replace('["', "").replace('"]', "").replace('"', "").split(', ')
                updated_data = tuple(item)
        # print(f"updated_data: {updated_data}")
        ReturnData[0] = {
            'id': updated_data[0],
            'formatted_address': updated_data[1],
            'formatted_phone_number': updated_data[2],
            'name': updated_data[3],
            'opening_hours': updated_data[4],
            'url': updated_data[5],
            'rating': updated_data[6],
            'wheelchair_accessible_entrance': updated_data[7],
            'user_ratings_total': updated_data[8],
            'class': updated_data[9],
            'photos': updated_data[10],
            'lat': updated_data[11],
            'lng': updated_data[12],
            'website': updated_data[13],
        }
    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
        return False, f"MySQL錯誤: {err}"
    return ReturnData
