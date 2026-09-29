import math
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import mysql.connector


# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config

# 2023 年的做法是用 Selenium 爬 Google Maps 路線頁，頁面結構一改就會失效，因此改為選用（USE_GMAPS_SCRAPER=1）。
# 未啟用或爬取失敗時，以直線距離估算開車時間，讓行程編排仍可運作。
USE_GMAPS_SCRAPER = os.getenv("USE_GMAPS_SCRAPER", "0") == "1"


def estimate_drive(aData, bData):
    """(lat, lng) -> (lat, lng): 回傳 (估計道路公里數, 估計開車分鐘數)。"""
    lat1, lng1, lat2, lng2 = (float(x) for x in (aData[0], aData[1], bData[0], bData[1]))
    p = math.pi / 180
    a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lng2 - lng1) * p)) / 2
    km = round(12742 * math.asin(math.sqrt(a)) * 1.3, 1)  # 道路距離約為直線距離的 1.3 倍
    total = max(5, round(km / (25 if km < 5 else 40) * 60))  # 市區約 25 km/h、郊區約 40 km/h
    return km, total


def _estimate_drive(aData, bData, end_date, hours, minutes):
    km, total = estimate_drive(aData, bData)
    h, m = divmod(total, 60)
    timeStr = f"{h}小時{m}分" if h and m else (f"{h}小時" if h else f"{m}分")
    end = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    next_start = end + timedelta(hours=h, minutes=m)
    return {
        'notDrive': False,
        'vehicle': '開車',
        'time': timeStr,
        'distance': km,
        'estimated': True,
        'NextTripStartTime': next_start,
        'NextTripEndTime': next_start + timedelta(hours=hours, minutes=minutes),
    }


def _scrape_google_maps(url, end_date, hours, minutes):
    ReturnData = []
    driver = None
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)

        i = 1
        found_drive = False
        while True:
            vehicle_xpath = f'/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[{i}]/span/span'
            time_xpath = f'/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[{i}]/div[1]/div/div[1]/div[1]'
            time2_xpath = f'/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[{i}]/div[1]/div/div[1]/div'
            distance_xpath = f'/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[{i}]/div[1]/div/div[1]/div[2]/div'

            vehicle_element = driver.find_element(by='xpath', value=vehicle_xpath) if driver.find_elements(by='xpath', value=vehicle_xpath) else None
            time_element = driver.find_element(by='xpath', value=time_xpath) if driver.find_elements(by='xpath', value=time_xpath) else None
            time_element2 = driver.find_element(by='xpath', value=time2_xpath) if driver.find_elements(by='xpath', value=time2_xpath) else None
            distance_element = driver.find_element(by='xpath', value=distance_xpath) if driver.find_elements(by='xpath', value=distance_xpath) else None

            if not vehicle_element:
                break

            vehicle = vehicle_element.get_attribute('aria-label')

            if vehicle == '開車':
                found_drive = True

            if found_drive:
                if time_element:
                    timeStr = time_element.text.replace(' ', '')
                else:
                    timeStr = time_element2.text.replace(' ', '')
                distance_str = distance_element.text
                distance = float(distance_str.replace('公里', '').replace('公尺', '').replace(',', ''))

                if '小時' in timeStr and '分' in timeStr:
                    time = timeStr.replace('小時', ':').replace('分', '')
                    time = datetime.strptime(time, '%H:%M')
                elif '小時' in timeStr:
                    time = timeStr.replace('小時', ':00')
                    time = datetime.strptime(timeStr, '%H:%M')
                else:
                    time = datetime.strptime(timeStr, '%M分')

                end_date_str = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
                if vehicle == '開車':
                    ReturnData.append({
                        'notDrive': False,
                        'vehicle': vehicle,
                        'time': timeStr,
                        'distance': distance,
                        'NextTripStartTime': datetime(
                            end_date_str.year,
                            end_date_str.month,
                            end_date_str.day,
                            end_date_str.hour,
                            end_date_str.minute
                        ) + timedelta(hours=time.hour, minutes=time.minute),
                        'NextTripEndTime': datetime(
                            end_date_str.year,
                            end_date_str.month,
                            end_date_str.day,
                            end_date_str.hour,
                            end_date_str.minute
                        ) + timedelta(hours=time.hour, minutes=time.minute) + timedelta(hours=hours, minutes=minutes)
                    })
            i += 1
        if not found_drive:
            print('not found drive')
            vehicle_xpath = '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div/span/span'
            time_xpath = '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div/div[1]/div/div[1]/div[1]'
            distance_xpath = '/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div/div[1]/div/div[1]/div[2]'

            vehicle_element = driver.find_element(by='xpath', value=vehicle_xpath) if driver.find_elements(by='xpath', value=vehicle_xpath) else None
            time_element = driver.find_element(by='xpath', value=time_xpath) if driver.find_elements(by='xpath', value=time_xpath) else None
            distance_element = driver.find_element(by='xpath', value=distance_xpath) if driver.find_elements(by='xpath', value=distance_xpath) else None

            vehicle = vehicle_element.get_attribute('aria-label')

            if not vehicle_element or not time_element or not distance_element and not time_element2:
                print('not found any element')
            timeStr = time_element.text.replace(' ', '')
            distance_str = distance_element.text

            if '小時' in timeStr and '分' in timeStr:
                time = timeStr.replace('小時', ':').replace('分', '')
                time = datetime.strptime(time, '%H:%M')
            elif '小時' in timeStr:
                time = timeStr.replace('小時', ':00')
                time = datetime.strptime(timeStr, '%H:%M')
            else:
                time = datetime.strptime(timeStr, '%M分')

            end_date_str = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            ReturnData.append({
                'notDrive': True,
                'vehicle': vehicle,
                'time': time,
                'distance': distance_str,
                'NextTripStartTime': datetime(
                    end_date_str.year,
                    end_date_str.month,
                    end_date_str.day,
                    end_date_str.hour,
                    end_date_str.minute
                ) + timedelta(hours=time.hour, minutes=time.minute),
                'NextTripEndTime': datetime(
                    end_date_str.year,
                    end_date_str.month,
                    end_date_str.day,
                    end_date_str.hour,
                    end_date_str.minute
                ) + timedelta(hours=time.hour, minutes=time.minute) + timedelta(hours=hours, minutes=minutes)
            })
    except Exception as e:
        print(f"Google Maps scraping failed: {e}")
    finally:
        if driver is not None:
            driver.quit()
    return ReturnData


def getDistanceNtime(aID, aType, aTrip, bID, bType, bTrip, end_date, hours=0, minutes=0):
    # 取得起點與終點經緯度
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute(f'SELECT lat, lng FROM `{aType}Data` WHERE id = %s;', (aTrip,))
    aData = cursor.fetchone()
    cursor.execute(f'SELECT lat, lng FROM `{bType}Data` WHERE id = %s;', (bTrip,))
    bData = cursor.fetchone()

    url = f"https://www.google.com.tw/maps/dir/{aData[0]},{aData[1]}/{bData[0]},{bData[1]}/"
    ReturnData = _scrape_google_maps(url, end_date, hours, minutes) if USE_GMAPS_SCRAPER else []
    if not any(data.get('vehicle') == '開車' for data in ReturnData):
        ReturnData = [_estimate_drive(aData, bData, end_date, hours, minutes)]

    drive_data = [data for data in ReturnData if data['vehicle'] == '開車']

    if drive_data:
        # 以時間排序
        drive_data = sorted(drive_data, key=lambda x: x['time'])
        drive_data = [drive_data[0]]

        # 取出時間資料並分為時與分
        hours = 0
        minutes = 0
        for data in drive_data:
            if '小時' in data['time'] and '分' in data['time']:
                data['time'] = data['time'].replace('小時', ':').replace('分', '')
                data['time'] = datetime.strptime(data['time'], '%H:%M')
                hours = data['time'].hour
                minutes = data['time'].minute
            elif '小時' in data['time'] and '分' not in data['time']:
                data['time'] = data['time'].replace('小時', ':00')
                data['time'] = datetime.strptime(data['time'], '%H:%M')
                hours = data['time'].hour
                minutes = data['time'].minute
            else:
                data['time'] = datetime.strptime(data['time'], '%M分')
                minutes = data['time'].minute

    sql = 'UPDATE `trip` SET nextHours = %s, nextMinutes = %s WHERE trip = %s AND type = %s AND id = %s ;'
    cursor.execute(sql, (hours, minutes, aTrip, aType, aID))
    conn.commit()

    for data in ReturnData:
        if "NextTripStartTime" in data and "NextTripEndTime" in data:
            data["NextTripStartTime"] = data["NextTripStartTime"].strftime("%Y-%m-%d %H:%M:%S")
            data["NextTripEndTime"] = data["NextTripEndTime"].strftime("%Y-%m-%d %H:%M:%S")
            sql = 'UPDATE `trip` SET startDate = %s, endDate = %s WHERE trip = %s AND type = %s AND id = %s ;'
            cursor.execute(sql, (data["NextTripStartTime"], data["NextTripEndTime"], bTrip, bType, bID))
            conn.commit()

    conn.close()
    return True, drive_data if drive_data else ReturnData
