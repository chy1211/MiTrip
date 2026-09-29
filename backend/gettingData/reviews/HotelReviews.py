from datetime import datetime
import mysql.connector

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config


# 新增評論
def addHotelReview(hotelId, userId, text, userRating):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    try:
        # 定義SQL插入語句
        sql = 'INSERT INTO HotelReviews (hotelID, userID, time, text, userRating) VALUES (%s, %s, %s, %s, %s);'
        val = (hotelId, userId, datetime.now(), text, userRating)

        # 執行SQL插入
        cursor.execute(sql, val)

        # 提交事務
        conn.commit()

    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


# 查詢(依飯店ID)
def getHotelReviews(hotelId):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    print(f'gHRev酒店ID: {hotelId}')
    data = []
    try:
        # 定義SQL查詢
        sql = 'SELECT textID, userID, time, text, userRating FROM HotelReviews WHERE hotelID = %s;'
        val = (hotelId,)

        # 執行SQL查詢
        cursor.execute(sql, val)

        # 獲取查詢結果
        results = cursor.fetchall()

        # 輸出評論資訊
        for row in results:
            textID, userID, time, text, userRating = row
            data.append((textID, userID, time, text, userRating))

    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")

    finally:
        cursor.close()
        conn.close()
    return data


# 查詢評論（依照使用者ID）
def getHotelReviewsByUserId(userId):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    returnData = {}

    try:
        # 定義SQL查詢語句
        sql = 'SELECT textID, hotelID, time, text, userRating FROM HotelReviews WHERE userID = %s;'
        val = (userId,)

        # 執行SQL查詢
        cursor.execute(sql, val)

        # 獲取查詢結果
        results = cursor.fetchall()
        # 輸出評論資訊
        for i in range(len(results)):
            sql = 'SELECT name, photos FROM HotelData WHERE id = %s;'
            val = (results[i][1],)
            cursor.execute(sql, val)
            hotelInfo = cursor.fetchone()
            parsed_date = datetime.strptime(str(results[i][2]), "%Y-%m-%d")
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            returnData[i] = {
                "dataType": "hotel",
                "textID": results[i][0],
                "hotelID": results[i][1],
                "time": formatted_date,
                "text": results[i][3],
                "userRating": results[i][4],
                "name": hotelInfo[0],
                "photos": hotelInfo[1],
            }

    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")

    finally:
        cursor.close()
        conn.close()

    return returnData


# 修改評論
def updateHotelReview(textId, newText, newUserRating):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    try:
        # 定義SQL更新語句
        sql = 'UPDATE HotelReviews SET text = %s, userRating = %s WHERE textID = %s;'
        val = (newText, newUserRating, textId)

        # 執行SQL更新
        cursor.execute(sql, val)

        # 提交事務
        conn.commit()

    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


# 刪除評論
def deleteHotelReview(textId):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    try:
        # 定義SQL刪除語句
        sql = 'DELETE FROM HotelReviews WHERE textID = %s;'
        val = (textId,)

        # 執行SQL刪除
        cursor.execute(sql, val)

        # 提交事務
        conn.commit()
        print(f"Deleted {cursor.rowcount} row(s)")

    except mysql.connector.Error as err:
        print(f"MySQL錯誤: {err}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
