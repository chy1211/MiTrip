import mysql.connector
from collections import OrderedDict
import sys
from tools.geo import get_bounding_box
from tools.isOpening import is_opening_hours
from recommendedSystem.itemBase.itemBase_Hotel import getSimilarHotelById
from recommendedSystem.userBase.userBase_hotel import getSimilarUserById
from recommendedSystem.collaborativeFiltering.collaborativeFiltering_Hotel import collaborativeFiltering
import json
# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config


def check_user_preferences(user_id):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    try:
        sql = 'SELECT * FROM `userPreferences` WHERE `userID` = %s LIMIT 1;'
        val = (user_id, )
        cursor.execute(sql, val)
        userPreferences = cursor.fetchone()
        if userPreferences:
            # print(f"使用者{user_id}的偏好存在")
            return True
        else:
            # print(f"使用者{user_id}的偏好不存在")
            return None
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


def check_browsing_history(user_id):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    try:
        sql = 'SELECT `history` FROM `browsingHistory` WHERE `type` = "hotel" AND `userID` = %s ORDER BY time DESC LIMIT 1;'
        val = (user_id, )
        cursor.execute(sql, val)
        latest_record = cursor.fetchone()
        if latest_record:
            # print(f"最新一筆瀏覽紀錄: {int(latest_record[0])}")
            return int(latest_record[0])
        else:
            # print(f"使用者{user_id}沒有瀏覽紀錄")
            return None
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


def check_trip_history(user_id):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    try:
        sql = 'SELECT trip FROM trip WHERE userID = %s AND type = "Hotel" ORDER BY id DESC LIMIT 1;'
        val = (user_id, )
        cursor.execute(sql, val)
        latest_record = cursor.fetchone()
        if latest_record:
            # print(f"使用者{user_id}最新一筆加入行程紀錄: {int(latest_record[0])}")
            return int(latest_record[0])
        else:
            # print(f"使用者{user_id}沒有任何加入行程紀錄")
            return None
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


def merge_and_weight(uBR=None, iBR=None, cF=None, weight_a=0.1, weight_b=0.4, weight_c=0.5):
    merged_dict = OrderedDict()

    if uBR:
        print(f"使用者相似度資料有{len(uBR)}筆")
        # 合併A的結果
        for item_a in uBR:
            merged_dict[item_a] = merged_dict.get(item_a, 0) + weight_a

    if iBR:
        print(f"住宿相似度資料有{len(iBR)}筆")
        # 合併B的結果
        for item_b in iBR:
            merged_dict[item_b] = merged_dict.get(item_b, 0) + weight_b

    if cF:
        print(f"行程相似度資料有{len(cF)}筆")
        # 合併C的結果
        for item_c in cF:
            merged_dict[item_c] = merged_dict.get(item_c, 0) + weight_c

    # 根據加權值降序排序
    merged_result = sorted(merged_dict, key=lambda x: merged_dict[x], reverse=True)
    # print(merged_result)

    return merged_result


def getHotelRec(userId, lat, lng, last=None, top_n=150, radius=5):
    Radius = get_bounding_box(lat, lng, radius)
    print(f"\n使用者{userId}正在取得住宿推薦...\n")
    trip = check_trip_history(userId)
    history = check_browsing_history(userId)

    #檢查使用者偏好是否存在
    if check_user_preferences(userId):
        userBaseResult = getSimilarUserById(int(userId), Radius['south'], Radius['north'], Radius['west'], Radius['east'])
        print("user_base used.")
    else:
        userBaseResult = None

    #檢查是否有最後一次的瀏覽紀錄
    if last:
        itemBaseResult = getSimilarHotelById(last, top_n, Radius['south'], Radius['north'], Radius['west'], Radius['east'])
        print("item_base used.")
    else:
        if history:
            itemBaseResult = getSimilarHotelById(history, top_n, Radius['south'], Radius['north'], Radius['west'], Radius['east'])
            print("item_base used.")
        else:
            itemBaseResult = None

    #檢查是否有加入行程紀錄
    if trip:
        print("collaborative_filtering used.")
        cf = collaborativeFiltering(trip, history, Radius['south'], Radius['north'], Radius['west'], Radius['east'])
    else:
        cf = None
    print("\n正在進行排序...\n")
    # 使用 merge_and_weight 函數進行排序
    sorted_recommendations = merge_and_weight(userBaseResult, itemBaseResult, cf)
    # print(f"sorted_recommendations: {sorted_recommendations}")
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    try:
        ReturnData = {}
        if sorted_recommendations:
            # 將排序後的推薦住宿 ID 列表轉換成 SQL 中的參數形式
            placeholders = ', '.join(['%s'] * len(sorted_recommendations))
            query = f'SELECT `id`, `name`, `rating`, `class`, `lat`, `lng`, `photos` FROM HotelData WHERE `id` IN ({placeholders}) ORDER BY FIELD(`id`, {placeholders})'
            cursor.execute(query, sorted_recommendations * 2)  # 將排序後的推薦餐廳 ID 列表複製一次用於 FIELD 函數
            data = cursor.fetchall()
        else:
            query = 'SELECT `id`, `name`,  `rating`, `class`, `lat`, `lng`, `photos` FROM HotelData WHERE `lat` BETWEEN %s AND %s AND `lng` BETWEEN %s AND %s'
            val = (Radius['south'], Radius['north'], Radius['west'], Radius['east'])
            cursor.execute(query, val)
            data = cursor.fetchall()
        for i in range(len(data)):
            item = list(data[i])
            if item[3]:
                item[3] = json.loads(item[3])["class"]
                data[i] = tuple(item)
        for i in range(len(data)):
            if i < top_n:
                ReturnData[i] = {
                    'id': data[i][0],
                    'name': data[i][1],
                    'rating': data[i][2],
                    'class': data[i][3],
                    'lat': data[i][4],
                    'lng': data[i][5],
                    'photos': data[i][6],
                }
            else:
                break
    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
        return False, f"MySQL錯誤: {err}"
    finally:
        cursor.close()
        conn.close()
        print(f"\n住宿推薦完成，共{len(ReturnData)}筆資料\n")
        return ReturnData


# print(getHotelRec(176, 22.774424, 120.399112))
