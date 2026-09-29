import mysql.connector
from collections import OrderedDict
from tools.geo import get_bounding_box
from recommendedSystem.itemBase.itemBase_Attraction import getSimilarAttractionById
from recommendedSystem.userBase.userBase_attraction import getSimilarUserById
from recommendedSystem.collaborativeFiltering.collaborativeFiltering_attraction import collaborativeFiltering

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
            return True
        else:
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
        sql = 'SELECT `history` FROM `browsingHistory` WHERE `type` = "attraction" AND `userID` = %s ORDER BY time DESC LIMIT 1;'
        val = (user_id, )
        cursor.execute(sql, val)
        latest_record = cursor.fetchone()
        if latest_record:
            return int(latest_record[0])
        else:
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
        sql = 'SELECT trip FROM trip WHERE userID = %s AND type = "Attraction" ORDER BY id DESC LIMIT 1;'
        val = (user_id, )
        cursor.execute(sql, val)
        latest_record = cursor.fetchone()
        if latest_record:
            return int(latest_record[0])
        else:
            return None
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


def merge_and_weight(uBR=None, iBR=None, cF=None, weight_a=0.1, weight_b=0.4, weight_c=0.5):
    merged_dict = OrderedDict()

    if uBR:
        for item_a in uBR:
            merged_dict[item_a] = merged_dict.get(item_a, 0) + weight_a

    if iBR:
        for item_b in iBR:
            merged_dict[item_b] = merged_dict.get(item_b, 0) + weight_b

    if cF:
        for item_c in cF:
            merged_dict[item_c] = merged_dict.get(item_c, 0) + weight_c

    merged_result = sorted(merged_dict, key=lambda x: merged_dict[x], reverse=True)
    return merged_result


def getAttractionRec(userId, lat, lng, last=None, top_n=150, radius=5):
    Radius = get_bounding_box(lat, lng, radius)
    print(f"\n使用者{userId}正在取得景點推薦...\n")
    trip = check_trip_history(userId)
    history = check_browsing_history(userId)

    if check_user_preferences(userId):
        userBaseResult = getSimilarUserById(int(userId), Radius['south'], Radius['north'], Radius['west'], Radius['east'])
        print("user_base used.")
    else:
        userBaseResult = None

    if last:
        itemBaseResult = getSimilarAttractionById(last, top_n, Radius['south'], Radius['north'], Radius['west'], Radius['east'])
        print("item_base used.")
    else:
        if history:
            itemBaseResult = getSimilarAttractionById(history, top_n, Radius['south'], Radius['north'], Radius['west'], Radius['east'])
            print("item_base used.")
        else:
            itemBaseResult = None

    if trip:
        print("collaborative_filtering used.")
        cf = collaborativeFiltering(trip, history, Radius['south'], Radius['north'], Radius['west'], Radius['east'])
    else:
        cf = None
    print("\n正在進行排序...\n")
    sorted_recommendations = merge_and_weight(userBaseResult, itemBaseResult, cf)

    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    try:
        ReturnData = {}
        if sorted_recommendations:
            placeholders = ', '.join(['%s'] * len(sorted_recommendations))
            query = f'SELECT `id`, `name`, `rating`, `class`, `lat`, `lng`, `photos` FROM AttractionData WHERE `id` IN ({placeholders}) ORDER BY FIELD(`id`, {placeholders})'
            cursor.execute(query, sorted_recommendations * 2)
            data = cursor.fetchall()
        else:
            query = 'SELECT `id`, `name`, `rating`, `class`, `lat`, `lng`, `photos` FROM AttractionData WHERE `lat` BETWEEN %s AND %s AND `lng` BETWEEN %s AND %s'
            val = (Radius['south'], Radius['north'], Radius['west'], Radius['east'])
            cursor.execute(query, val)
            data = cursor.fetchall()

        for i in range(len(data)):
            item = list(data[i])
            if item[3]:
                item[3] = item[3].replace('{',"").replace('class',"").replace(': ',"").replace('["', "").replace('"]', "").replace('"', "").replace('}',"").split(', ')
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
        print(f"\n景點推薦完成，共{len(ReturnData)}筆資料\n")
        return ReturnData
