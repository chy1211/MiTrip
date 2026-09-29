import mysql.connector
import sys
from tools.isOpening import is_opening_hours
from datetime import datetime, timedelta


# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config


def insert_data(name, sDescribe, startDate, endDate, userID, privilege):
    print(f"Inserting data: {name}, {sDescribe}, {startDate}, {endDate}, {userID}, {privilege}")
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO `schedule` (name, sDescribe, startDate, endDate, userID, privilege)
        VALUES (%s, %s, %s, %s, %s, %s);
        ''', (name, sDescribe, startDate, endDate, userID, privilege))

        conn.commit()
        conn.close()

        return True, '行程表新增成功'
    except mysql.connector.Error as err:
        return False, f"Error: {err}"


def compare_fn(trip):
    on_day = trip.get('onDay', float('inf'))  # 如果 'onDay' 不存在，將其視為無窮大
    trip_type = trip.get('tripType', '')
    if trip_type == 'Days':
        return (0, on_day)  # 'Days' 元素應該在排序時被視為最小值
    else:
        return (1, on_day)  # 其他元素在排序時按照 'onDay' 的值排序


def get_schedule_and_trips_by_user_id(user_id):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM `schedule` WHERE userID = %s ORDER BY startDate;;', (user_id,))
        schedule_data = cursor.fetchall()

        formatted_data = {}
        for schedule in schedule_data:
            cursor.execute('SELECT * FROM `trip` WHERE scheduleID = %s ORDER BY startDate;;', (schedule[0],))
            trips_data = cursor.fetchall()

            formatted_trips = []
            for trip in trips_data:
                if trip[2] == 'Restaurant':
                    cursor.execute('SELECT id, name, rating, opening_hours, class FROM `RestaurantData` WHERE id = %s;', (trip[3],))
                    restaurant_data = cursor.fetchone()
                    if restaurant_data:
                        try:
                            current_trip_data = {
                                'tripID': trip[0],
                                'tripType': trip[2],
                                'restaurantID': restaurant_data[0],
                                'tripName': restaurant_data[1],
                                'rating': restaurant_data[2],
                                'class': restaurant_data[4],
                                'tripStartDate': str(trip[4]),
                                'tripEndDate': str(trip[5]),
                                'tripOpen': '營業中' if is_opening_hours(restaurant_data[3]) else '休息中'
                            }
                        except Exception as e:
                            print(f"Error processing restaurant data: {e}")
                            current_trip_data = {}
                    else:
                        current_trip_data = {}
                    formatted_trips.append(current_trip_data)
                elif trip[2] == 'Attraction':
                    cursor.execute('SELECT id, name, rating, opening_hours, class FROM `AttractionData` WHERE id = %s;', (trip[3],))
                    attraction_data = cursor.fetchone()
                    if attraction_data:
                        try:
                            current_trip_data = {
                                'tripID': trip[0],
                                'tripType': trip[2],
                                'attractionID': attraction_data[0],
                                'tripName': attraction_data[1],
                                'rating': attraction_data[2],
                                'class': attraction_data[4],
                                'tripStartDate': str(trip[4]),
                                'tripEndDate': str(trip[5]),
                                'tripOpen': '營業中' if is_opening_hours(attraction_data[3]) else '休息中'
                            }
                        except Exception as e:
                            print(f"Error processing attraction data: {e}")
                            current_trip_data = {}
                    else:
                        current_trip_data = {}
                    formatted_trips.append(current_trip_data)
                elif trip[2] == 'Hotel':
                    pass

            schedule_dict = {
                "scheduleID": schedule[0],
                "name": schedule[1],
                "sDescribe": schedule[2],
                "startDate": str(schedule[3]),
                "endDate": str(schedule[4]),
                "userID": schedule[5],
                "trip": formatted_trips
            }

            formatted_data[schedule[0]] = schedule_dict

        conn.close()

        return True, formatted_data

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False, f"Error: {err}"


def select_by_user_id(user_id):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM `schedule` WHERE userID = %s;', (user_id,))
        schedule_data = cursor.fetchall()

        formatted_data = {}
        for schedule in schedule_data:
            schedule_dict = {
                "scheduleID": schedule[0],
                "name": schedule[1],
                "sDescribe": schedule[2],
                "startDate": schedule[3].strftime('%Y-%m-%d'),
                "endDate": schedule[4].strftime('%Y-%m-%d'),
                "userID": schedule[5],
                "days": (schedule[4] - schedule[3]).days + 1,
                "privilege": schedule[6]
            }
            formatted_data[schedule[0]] = schedule_dict

        conn.close()

        return True, formatted_data
    except mysql.connector.Error as err:
        return False, f"Error: {err}"


def select_by_id(schedule_id):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        # 先生成天數的資料
        formatted_trips = []

        # 從資料庫撈取 schedule 的資料
        cursor.execute('SELECT startDate, endDate FROM schedule WHERE ID = %s;', (schedule_id,))
        schedule_dates = cursor.fetchone()

        if schedule_dates:
            start_date, end_date = schedule_dates

            # 計算天數差距
            max_day = (end_date - start_date).days + 1

            # 生成天數的資料
            for i in range(1, max_day + 1):
                current_date = start_date + timedelta(days=i - 1)
                formatted_trips.append({'onDay': i, 'tripName': f'第{i}天', 'tripType': 'Days', 'Date': str(current_date)})

            cursor.execute('SELECT * FROM `trip` WHERE scheduleID = %s ORDER BY startDate;', (schedule_id,))
            trips = cursor.fetchall()

            num = 1

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

                if trip[2] == 'Restaurant':
                    cursor.execute('SELECT id, name, photos, lat, lng FROM `RestaurantData` WHERE id = %s;', (trip[3],))
                    restaurant_data = cursor.fetchone()
                    if restaurant_data:
                        try:
                            current_trip_data = {
                                'tripID': trip[0],
                                'scheduleID': trip[1],
                                'tripType': trip[2],
                                'restaurantID': restaurant_data[0],
                                'tripName': restaurant_data[1],
                                'tripStartDate': str(trip[4]),
                                'tripEndDate': str(trip[5]),
                                'onDay': on_day,
                                'durationHours': hours,
                                'durationMinutes': minutes,
                                'photos': restaurant_data[2],
                                'lat': restaurant_data[3],
                                'lng': restaurant_data[4],
                                'toNextTripHours': trip[7],
                                'toNextTripMinutes': trip[8],
                                'currentTripNum': num
                            }
                        except Exception as e:
                            print(f"Error processing restaurant data: {e}")
                            current_trip_data = {}
                    else:
                        current_trip_data = {}
                    formatted_trips.append(current_trip_data)
                elif trip[2] == 'Attraction':
                    cursor.execute('SELECT id, name, photos, lat, lng FROM `AttractionData` WHERE id = %s;', (trip[3],))
                    attraction_data = cursor.fetchone()
                    if attraction_data:
                        try:
                            current_trip_data = {
                                'tripID': trip[0],
                                'scheduleID': trip[1],
                                'tripType': trip[2],
                                'attractionID': attraction_data[0],
                                'tripName': attraction_data[1],
                                'tripStartDate': str(trip[4]),
                                'tripEndDate': str(trip[5]),
                                'onDay': on_day,
                                'durationHours': hours,
                                'durationMinutes': minutes,
                                'photos': attraction_data[2],
                                'lat': attraction_data[3],
                                'lng': attraction_data[4],
                                'toNextTripHours': trip[7],
                                'toNextTripMinutes': trip[8],
                                'currentTripNum': num
                            }
                        except Exception as e:
                            print(f"Error processing attraction data: {e}")
                            current_trip_data = {}
                    else:
                        current_trip_data = {}
                    formatted_trips.append(current_trip_data)
                elif trip[2] == 'Hotel':
                    cursor.execute('SELECT id, name, photos, lat, lng FROM `HotelData` WHERE id = %s;', (trip[3],))
                    hotel_data = cursor.fetchone()
                    if hotel_data:
                        try:
                            current_trip_data = {
                                'tripID': trip[0],
                                'scheduleID': trip[1],
                                'tripType': trip[2],
                                'hotelID': hotel_data[0],
                                'tripName': hotel_data[1],
                                'tripStartDate': str(trip[4]),
                                'tripEndDate': str(trip[5]),
                                'onDay': on_day,
                                'durationHours': hours,
                                'durationMinutes': minutes,
                                'photos': hotel_data[2],
                                'lat': hotel_data[3],
                                'lng': hotel_data[4],
                                'toNextTripHours': trip[7],
                                'toNextTripMinutes': trip[8],
                                'currentTripNum': num
                            }
                        except Exception as e:
                            print(f"Error processing hotel data: {e}")
                            current_trip_data = {}
                    else:
                        current_trip_data = {}
                    formatted_trips.append(current_trip_data)
                num += 1
        conn.close()

    except mysql.connector.Error as err:
        return False, f"Error: {err}"

    finally:
        formatted_trips = sorted(formatted_trips, key=lambda x: x['onDay'])
        return True, formatted_trips


def update_schedule(event_id, new_name, new_start_date, new_end_date, new_description, new_privilege):
    print(f"Updating schedule: {event_id}, {new_name}, {new_start_date}, {new_end_date}, {new_description}, {new_privilege}")
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        # 使用 SET 子句更新多個欄位
        cursor.execute('''
            UPDATE `schedule`
            SET name = %s, startDate = %s, endDate = %s, sDescribe = %s, privilege = %s
            WHERE ID = %s;
        ''', (new_name, new_start_date, new_end_date, new_description, new_privilege, event_id))

        conn.commit()
        conn.close()

        return True, '行程表更新成功'
    except mysql.connector.Error as err:
        return False, f"Error: {err}"


def delete_schedule(event_id):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM `schedule` WHERE ID = %s;', (event_id,))

        conn.commit()
        conn.close()

        return True, '行程表刪除成功'
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
