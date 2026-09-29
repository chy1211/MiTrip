import mysql.connector
from collections import OrderedDict

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config


def getRecommendedHotelFromLastTrip(trip):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    try:
        sql = 'SELECT type, trip, COUNT(*) as occurrences FROM trip WHERE scheduleID IN ( SELECT scheduleID FROM trip WHERE scheduleID IN ( SELECT scheduleID FROM trip WHERE type = "Hotel" AND trip = %s ) AND type = "Hotel" AND trip != %s ) AND type = "Hotel" AND trip != %s GROUP BY type, trip ORDER BY occurrences DESC;'
        val = (trip, trip, trip)
        cursor.execute(sql, val)
        recommended_hotels = cursor.fetchall()
        if recommended_hotels:
            formatted_hotels = []
            for hotel in recommended_hotels:
                formatted_hotels.append(hotel[1])
            return formatted_hotels
        else:
            return None
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


def getRecommendedHotelFromHistory(history):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    try:
        sql = 'SELECT type, history, COUNT(*) as count FROM browsingHistory WHERE userID IN (SELECT userID FROM browsingHistory WHERE type = "hotel" AND history = %s) GROUP BY type, history ORDER BY count DESC;'
        val = (history,)
        cursor.execute(sql, val)
        recommended_hotels = cursor.fetchall()
        if recommended_hotels:
            formatted_hotels = []
            for hotel in recommended_hotels:
                formatted_hotels.append(hotel[1])
            return formatted_hotels
        else:
            return None
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


def merge_and_weight(trip=None, history=None, weight_a=0.6, weight_b=0.4):
    merged_dict = OrderedDict()

    if trip:
        # 合併A的結果
        for item_a in trip:
            merged_dict[item_a] = merged_dict.get(item_a, 0) + weight_a

    if history:
        # 合併B的結果
        for item_b in history:
            merged_dict[item_b] = merged_dict.get(item_b, 0) + weight_b

    # 根據加權值降序排序
    merged_result = sorted(merged_dict, key=lambda x: merged_dict[x], reverse=True)

    return merged_result


def collaborativeFiltering(trip, history, Rs, Rn, Rw, Re):
    merged_result = merge_and_weight(getRecommendedHotelFromLastTrip(trip), getRecommendedHotelFromHistory(history))
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    try:
        hotel_ids = ','.join(map(str, merged_result))
        sql = f'SELECT id FROM HotelData WHERE id IN({hotel_ids}) AND `lat` BETWEEN %s AND %s AND `lng` BETWEEN %s AND %s'
        val = (Rs, Rn, Rw, Re)
        cursor.execute(sql, val)
        recommended_hotels = cursor.fetchall()
        if recommended_hotels:
            formatted_hotels = []
            for hotel in recommended_hotels:
                formatted_hotels.append(hotel[0])
            return formatted_hotels
        else:
            return None
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


# print(collaborativeFiltering(4095, 2757, 22.72927342284951, 22.819574321854184, 120.35042276626433, 120.44780123373567))