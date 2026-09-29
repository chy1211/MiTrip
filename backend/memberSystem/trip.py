import mysql.connector
import sys
from tools.isOpening import is_opening_hours
from tools.distanceNtime import estimate_drive
from datetime import datetime, time, timedelta

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config

TRIP_TYPES = ('Restaurant', 'Attraction', 'Hotel')


def _place_position(cursor, trip_type, place_id):
    cursor.execute(f'SELECT lat, lng FROM `{trip_type}Data` WHERE id = %s;', (place_id,))
    return cursor.fetchone()


def insert_trip(scheduleID, trip_type, trip_id, user_id):
    if trip_type not in TRIP_TYPES:
        return False, f"Error: unknown trip type {trip_type}"
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute('SELECT startDate, endDate FROM `schedule` WHERE id = %s;', (scheduleID,))
        schedule = cursor.fetchone()
        start_date = schedule[0]
        # 接在目前最後一站之後（最後一站結束時間 + 預估車程）；空行程則從行程開始時間起算。
        # 2023 版一律放在行程開始時間，會與當天第一站重疊。
        cursor.execute('SELECT id, type, trip, endDate FROM `trip` WHERE scheduleID = %s ORDER BY endDate DESC LIMIT 1;', (scheduleID,))
        last = cursor.fetchone()
        if last:
            a, b = _place_position(cursor, last[1], last[2]), _place_position(cursor, trip_type, trip_id)
            travel = estimate_drive(a, b)[1] if a and b else 0
            start_date = last[3] + timedelta(minutes=travel)
            h, m = divmod(travel, 60)
            cursor.execute('UPDATE `trip` SET nextHours = %s, nextMinutes = %s WHERE id = %s;', (h, m, last[0]))
        end_date = start_date + timedelta(hours=1)
        cursor.execute('''
        INSERT INTO `trip` (scheduleID, type, trip, startDate, endDate, userID)
        VALUES (%s, %s, %s, %s, %s, %s);
        ''', (scheduleID, trip_type, trip_id, start_date, end_date, user_id))

        conn.commit()
        conn.close()

        return True, '行程新增成功'
    except mysql.connector.Error as err:
        return False, f"Error: {err}"


def select_trip_by_user_id(user_id):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM `trip` WHERE userID = %s ORDER BY startDate;', (user_id,))
        trips = cursor.fetchall()

        formatted_trips = []
        for trip in trips:
            cursor.execute('SELECT startDate FROM `schedule` WHERE id = %s;', (trip[1],))
            schedule = cursor.fetchone()
            startDate = schedule[0].date()  # 只取日期部分
            if isinstance(trip[4], str):
                trip_start_date = datetime.strptime(trip[4], '%Y-%m-%d %H:%M:%S')
                trip_start_date = trip_start_date.date()  # 只取日期部分
            else:
                trip_start_date = trip[4].date()

            on_day = (trip_start_date - startDate).days + 1
            # 計算停留時間
            duration = trip[5] - trip[4]

            # 格式化停留時間為「時分」形式
            hours, remainder = divmod(duration.seconds, 3600)
            minutes = remainder // 60
            duration = f"{hours}時{minutes}分"
            if trip[2] == 'Restaurant':
                cursor.execute('SELECT id, name, rating, opening_hours, class, photos, lat, lng FROM `RestaurantData` WHERE id = %s;', (trip[3],))
                restaurant_data = cursor.fetchone()
                if restaurant_data:
                    try:
                        current_trip_data = {
                            'tripID': trip[0],
                            'scheduleID': trip[1],
                            'tripType': trip[2],
                            'restaurantID': restaurant_data[0],
                            'tripName': restaurant_data[1],
                            'rating': restaurant_data[2],
                            'class': restaurant_data[4],
                            'tripStartDate': str(trip[4]),
                            'tripEndDate': str(trip[5]),
                            'tripOpen': '營業中' if is_opening_hours(restaurant_data[3]) else '休息中',
                            'onDay': on_day,
                            'duration': duration,
                            'photos': restaurant_data[5],
                            'lat': restaurant_data[6],
                            'lng': restaurant_data[7]
                        }
                    except Exception as e:
                        print(f"Error processing restaurant data: {e}")
                        current_trip_data = {}
                else:
                    current_trip_data = {}
                formatted_trips.append(current_trip_data)
            elif trip[2] == 'Attraction':
                cursor.execute('SELECT id, name, rating, opening_hours, class, photos, lat, lng FROM `AttractionData` WHERE id = %s;', (trip[3],))
                attraction_data = cursor.fetchone()
                if attraction_data:
                    try:
                        current_trip_data = {
                            'tripID': trip[0],
                            'scheduleID': trip[1],
                            'tripType': trip[2],
                            'attractionID': attraction_data[0],
                            'tripName': attraction_data[1],
                            'rating': attraction_data[2],
                            'class': attraction_data[4],
                            'tripStartDate': str(trip[4]),
                            'tripEndDate': str(trip[5]),
                            'tripOpen': '營業中' if is_opening_hours(attraction_data[3]) else '休息中',
                            'onDay': on_day,
                            'photos': attraction_data[5],
                            'lat': attraction_data[6],
                            'lng': attraction_data[7]
                        }
                    except Exception as e:
                        print(f"Error processing attraction data: {e}")
                        current_trip_data = {}
                else:
                    current_trip_data = {}
                formatted_trips.append(current_trip_data)
            elif trip[2] == 'Hotel':
                pass
        conn.close()
        return True, formatted_trips

    except mysql.connector.Error as err:
        return False, f"Error: {err}"


def select_trip_by_id(trip_id):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM `trip` WHERE id = %s;', (trip_id,))
        trip = cursor.fetchone()
        
        # 計算停留時間
        duration = trip[5] - trip[4]
        # 格式化停留時間為「時分」形式
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = remainder // 60
        if trip[2] == 'Restaurant':
            cursor.execute('SELECT id, name, rating, opening_hours, class, photos FROM `RestaurantData` WHERE id = %s;', (trip[3],))
            restaurant_data = cursor.fetchone()
            if restaurant_data:
                try:
                    formatted_data = {
                        'tripID': trip[0],
                        'tripType': trip[2],
                        'restaurantID': restaurant_data[0],
                        'tripName': restaurant_data[1],
                        'rating': restaurant_data[2],
                        'class': restaurant_data[4],
                        'photos': restaurant_data[5],
                        'tripStartDate': str(trip[4]),
                        'tripEndDate': str(trip[5]),
                        'toNextTripHours': trip[7],
                        'toNextTripMinutes': trip[8],
                        'durationHours': hours,
                        'durationMinutes': minutes,
                        'tripOpen': '營業中' if is_opening_hours(restaurant_data[3]) else '休息中'
                    }
                except Exception as e:
                    print(f"Error processing restaurant data: {e}")
                    formatted_data = {}
        elif trip[2] == 'Attraction':
            cursor.execute('SELECT id, name, rating, opening_hours, class, photos FROM `AttractionData` WHERE id = %s;', (trip[3],))
            attraction_data = cursor.fetchone()
            if attraction_data:
                try:
                    formatted_data = {
                        'tripID': trip[0],
                        'tripType': trip[2],
                        'attractionID': attraction_data[0],
                        'tripName': attraction_data[1],
                        'rating': attraction_data[2],
                        'class': attraction_data[4],
                        'photos': attraction_data[5],
                        'tripStartDate': str(trip[4]),
                        'tripEndDate': str(trip[5]),
                        'toNextTripHours': trip[7],
                        'toNextTripMinutes': trip[8],
                        'durationHours': hours,
                        'durationMinutes': minutes,
                        'tripOpen': '營業中' if is_opening_hours(attraction_data[3]) else '休息中'
                    }
                except Exception as e:
                    print(f"Error processing attraction data: {e}")
                    formatted_data = {}
        elif trip[2] == 'Hotel':
            cursor.execute('SELECT id, name, rating, opening_hours, class, photos FROM `HotelData` WHERE id = %s;', (trip[3],))
            hotel_data = cursor.fetchone()
            if hotel_data:
                try:
                    formatted_data = {
                        'tripID': trip[0],
                        'tripType': trip[2],
                        'hotelID': hotel_data[0],
                        'tripName': hotel_data[1],
                        'rating': hotel_data[2],
                        'class': hotel_data[4],
                        'photos': hotel_data[5],
                        'tripStartDate': str(trip[4]),
                        'tripEndDate': str(trip[5]),
                        'toNextTripHours': trip[7],
                        'toNextTripMinutes': trip[8],
                        'durationHours': hours,
                        'durationMinutes': minutes,
                        'tripOpen': '營業中' if is_opening_hours(hotel_data[3]) else '休息中'
                    }
                except Exception as e:
                    print(f"Error processing hotel data: {e}")
                    formatted_data = {}
        conn.close()

        return True, formatted_data

    except mysql.connector.Error as err:
        return False, f"Error: {err}"


def update_trip(trip_id, newScheduleID, new_type, new_trip, new_start_date, new_end_date, new_user_id):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE `trip`
            SET scheduleID = %s, type = %s, trip = %s, startDate = %s, endDate = %s, userID = %s
            WHERE ID = %s;
        ''', (newScheduleID, new_type, new_trip, new_start_date, new_end_date, new_user_id, trip_id))

        conn.commit()
        conn.close()

        return True, '行程更新成功'

    except mysql.connector.Error as err:
        return False, f"Error: {err}"


def delete_trip(trip_id):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM `trip` WHERE ID = %s;', (trip_id,))

        conn.commit()
        conn.close()
        return True, '行程刪除成功'

    except mysql.connector.Error as err:
        return False, f"Error: {err}"


def update_time(trip_id, new_start_date, durationHour, durationMinute):
    duration = timedelta(hours=durationHour, minutes=durationMinute)
    new_start_date = datetime.strptime(new_start_date, '%Y-%m-%d %H:%M:%S')
    new_end_date = new_start_date + duration
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE `trip`
            SET startDate = %s, endDate = %s
            WHERE ID = %s;
        ''', (new_start_date, new_end_date, trip_id))

        conn.commit()
        conn.close()

        return True, '行程更新成功'

    except mysql.connector.Error as err:
        return False, f"Error: {err}"


def reflow_schedule(schedule_id, order):
    """依拖曳後的新順序重排整個行程的時間。

    order: [{"tripID": 12, "day": 1}, ...]，已依畫面順序排列。
    每天第一站沿用該天原本最早的出發時間（沒有則 09:00），之後每一站 = 上一站結束 + 預估車程，
    停留時間不變，並重算每一段的 nextHours / nextMinutes。
    2023 版拖曳後只重算前後兩站，後續站點不會順延，容易重疊或被推到別天。
    """
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute('SELECT startDate FROM `schedule` WHERE id = %s;', (schedule_id,))
        row = cursor.fetchone()
        if not row:
            return False, '找不到行程表'
        first_date = row[0].date()
        cursor.execute('SELECT id, type, trip, startDate, endDate FROM `trip` WHERE scheduleID = %s;', (schedule_id,))
        trips = {r[0]: r for r in cursor.fetchall()}

        # 各天原本的出發時間（重排前該天最早一站的時刻）
        day_start = {}
        for _, _, _, start, _ in trips.values():
            day = (start.date() - first_date).days + 1
            if day not in day_start or start.time() < day_start[day]:
                day_start[day] = start.time()

        days = {}
        for item in order:
            trip_id, day = int(item['tripID']), int(item['day'])
            if trip_id in trips:
                days.setdefault(day, []).append(trips[trip_id])

        for day, seq in days.items():
            t = datetime.combine(first_date + timedelta(days=day - 1), day_start.get(day, time(9, 0)))
            for i, (trip_id, trip_type, place_id, start, end) in enumerate(seq):
                new_end = t + (end - start)
                travel = None
                if i + 1 < len(seq):
                    a = _place_position(cursor, trip_type, place_id)
                    b = _place_position(cursor, seq[i + 1][1], seq[i + 1][2])
                    travel = estimate_drive(a, b)[1] if a and b else 0
                h, m = divmod(travel, 60) if travel is not None else (None, None)
                cursor.execute('UPDATE `trip` SET startDate = %s, endDate = %s, nextHours = %s, nextMinutes = %s WHERE id = %s;',
                               (t, new_end, h, m, trip_id))
                t = new_end + timedelta(minutes=travel or 0)

        conn.commit()
        conn.close()
        return True, '行程已重新排序'
    except (mysql.connector.Error, KeyError, ValueError, TypeError) as err:
        return False, f"Error: {err}"
