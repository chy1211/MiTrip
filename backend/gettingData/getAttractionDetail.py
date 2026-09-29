import mysql.connector
import json
import sys
from tools.isOpening import is_opening_hours

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config

def getAttractionDetail(user_id, attraction_id):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    print(f"gAD使用者ID: {user_id}")
    print(f"gAD景點ID: {attraction_id}")
    try:
        ReturnData = {}
        sql = 'INSERT INTO `browsingHistory` (userID, type, history) VALUES (%s, %s, %s);'
        data = (user_id, "attraction", attraction_id)
        cursor.execute(sql, data)
        conn.commit()

        sql = 'SELECT id, formatted_address, formatted_phone_number, name, opening_hours, url, rating, user_ratings_total, class, photos, lat, lng, website FROM `AttractionData` WHERE id = %s;'
        val = (attraction_id, )
        cursor.execute(sql, val)
        data = cursor.fetchall()
        for i in range(len(data)):
            item = list(data[i])  # Convert the tuple to a list

            # Check if opening hours are provided
            if item[4]:
                ifOpening = is_opening_hours(item[4])
                if ifOpening:
                    text = "營業中"
                elif ifOpening is False:
                    text = "休息中"
                item.append(text)
                
                # Parse JSON if opening_hours is not NULL
                item[4] = json.loads(item[4])
                weekday_text = item[4]["weekday_text"]
                item[4] = weekday_text
                
            if item[8]:
                item[8] = item[8].replace('{',"").replace('class',"").replace(': ',"").replace('["', "").replace('"]', "").replace('"', "").replace('}',"").split(', ')

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
                'user_ratings_total': updated_data[7],
                'class': updated_data[8],
                'photos': updated_data[9],
                'lat': updated_data[10],
                'lng': updated_data[11],
                'website': updated_data[12],
            }
    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
        return False, f"MySQL錯誤: {err}"
    finally:
        cursor.close()
        conn.close()

    return ReturnData
