import mysql.connector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta

# MySQL連接參數
from config import MYSQL_CONFIG as mysql_config

cityData = {
    '新北市': {
        'longitude': 121.435985,
        'latitude': 25.0059765,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipO-RJfoq8UcXv6gpHRwksuS736txJXrYIfeSaFS=w408-h271-k-no'
    },
    '高雄市': {
        'longitude': 120.3110824,
        'latitude': 22.6167954,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipNV4nviVa2wu8Dd1e7jcik-HGeBaXMbzASVLl2R=w408-h306-k-no'
    },
    '台中市': {
        'longitude': 120.6670276,
        'latitude': 24.1408323,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipNIHn3pjAiWihMTDsmX7j-f9Vk1q36S5mQaadbX=w408-h306-k-no'
    },
    '台北市': {
        'longitude': 121.5553296,
        'latitude': 25.0476045,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipM3Ja6oI6z6OHNj2FsQ1m0IcDRhxX6exASbPner=w420-h240-k-no'
    },
    '桃園縣': {
        'longitude': 121.2168,
        'latitude': 24.93759,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipPDA0dwWr1kyMp-9of0BaigQBj7hRK8VMugeInK=w408-h304-k-no'
    },
    '台南市': {
        'longitude': 120.2513,
        'latitude': 23.1417,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipOvOj3HfscQNeD7gUkMeNTLpyOsUCjyt8KXvluN=w408-h271-k-no'
    },
    '彰化縣': {
        'longitude': 120.4818,
        'latitude': 23.99297,
        'photo': 'https://lh3.googleusercontent.com/gps-proxy/AFm_dcQFYOHb4RQ0ot0bkV8i4G5vwn2L9sfCXRjN1MRdF9SpXPYK7w4_yKOEDuLQ_RlWo-dRj8Sfl2fuLakCNj1k4m-L25NzLSCm9fibfY-FDKH9zQZ1at8swzcAIqQqOWUYeC9PeZwKlZKehJ4Ev5bEb3-xQO95baTBpZfNPwUjKokeUu08z7BGTy0=w408-h272-k-no'
    },
    '屏東縣': {
        'longitude': 120.4778912,
        'latitude': 22.6659077,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipPlomGZUy1hinCuKjct3IHFFmjwD3GWMsi--0Zl=w408-h306-k-no'
    },
    '雲林縣': {
        'longitude': 120.3897,
        'latitude': 23.75585,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipO0_c99VdDwxCKyZ9BE8Zch6smDgzk2nMMshbs=w426-h240-k-no'
    },
    '苗栗縣': {
        'longitude': 120.9417,
        'latitude': 24.48927,
        'photo': 'https://lh3.googleusercontent.com/gps-proxy/AFm_dcRKYzqGFPacoBfJsic2OpYwH9OTHXUwMoy6PyvyLm9rBIkRGXwLwZKvX3ux0vMHGwpcc5ejUoVLFWjw-aI84aOb8uAZDMWZbsDYzPb7VfkR0ooAtgNKS6lb61HBqasnw6Wp7dTsMU8DvWNJMt6zYUSFTsNJNbNgwN0S6S2e96ogeymSgtvussOJjQ=w408-h272-k-no'
    },
    '嘉義縣': {
        'longitude': 120.574,
        'latitude': 23.45889,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipNNgE1qGpIQ5oyXIWqkGe8Blfo-9BgTtl_dQvde=w426-h240-k-no'
    },
    '新竹縣': {
        'longitude': 121.1252,
        'latitude': 24.70328,
        'photo': 'https://lh3.googleusercontent.com/gps-proxy/AFm_dcR9ELxq9lGfj2pX9nvZF6xdk4yRIdQ10l-kI1_i-iyRfQ7MTVS6DQLUZZzMKtzIQp7bFexiVIBejva_gHyNTADHNDruHsi075URGBjpc4KyaLh2MeCAriiZmJ5wvKsRTlNL3_aamrUfu0fq9STD9vDb_IXyCt3gKVyBI4Yws5_H3y2aw3HAoCOxkg=w408-h272-k-no'
    },
    '南投縣': {
        'longitude': 120.8887505,
        'latitude': 23.9745557,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipOobRe4hhnhVjEe3hhf4fgCa_3Ct0bMOM29C2q0=w408-h312-k-no'
    },
    '宜蘭縣': {
        'longitude': 121.7195,
        'latitude': 24.69295,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipN-C4l5m1DlBE0Ud9sqa9XyfFcVB9AbPqTXyHXO=w408-h273-k-no'
    },
    '新竹市': {
        'longitude': 120.9647,
        'latitude': 24.80395,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipMqSdwl18QNzJCxc2Qc7Q-aLAEPo68Ezd5e7IqB=w426-h240-k-no'
    },
    '基隆市': {
        'longitude': 121.7081,
        'latitude': 25.10898,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipPEK6VWAdYDtxUixeD8-gHnGR0eppUAk3mNJqZA=w426-h240-k-no'
    },
    '花蓮縣': {
        'longitude': 121.3542,
        'latitude': 23.7569,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipNxutsi65g0ih2BEtH4U81_oYq7eatNuYrPfJ5U=w426-h240-k-no'
    },
    '嘉義市': {
        'longitude': 120.4473,
        'latitude': 23.47545,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipNYOo1_yx8_vyNLg3RMJZga-YWas3Ne1HpGhb7Y=w408-h271-k-no'
    },
    '台東縣': {
        'longitude': 120.9876,
        'latitude': 22.98461,
        'photo': 'https://lh3.googleusercontent.com/gps-proxy/AFm_dcS2vxeruOaBkJCkBJJtT1ntUBll6q0yGHwVISPCPrlLulxE5w8dG8318vIiABspZORkALqqL6t0JoCklwEFMq4bmcwIGYCAFi_mHoa49uIBoVmqIFMqOMwJ7ojtaIvWoES_A5zhNz6zzyXIZlLBNoyD3V8ednpm10CGifad-KkjfjwVkHz8gxiv=w408-h272-k-no'
    },
    '金門縣': {
        'longitude': 118.3186,
        'latitude': 24.43679,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipOSvay2yezV7QiJ4noq48q8OOl-u5BNoYrEj8QW=w408-h306-k-no'
    },
    '澎湖縣': {
        'longitude': 119.6151,
        'latitude': 23.56548,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipN1XGHAjrH3lF56AQ0F8s2-wo2Ft_6WWf5oi35l=w426-h240-k-no'
    },
    '連江縣': {
        'longitude': 119.5397,
        'latitude': 26.19737,
        'photo': 'https://lh5.googleusercontent.com/p/AF1QipPc2R01P0Ndx0Mzmlh7du_uuBSNQA_wgLGMKmwi=w408-h272-k-no'
    }
}

city = list(cityData.keys())
city = [c.replace('臺', '台') for c in city]


def checkHottestHistory():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    try:
        formatHottestHistory = []

        # Iterate over rankings (1st, 2nd, 3rd)
        for rank in range(1, 4):
            # Iterate over types (restaurant, attraction, hotel)
            types = ['restaurant', 'attraction', 'hotel']
            for history_type in types:
                # Select the top history for each type and rank
                sql = f'SELECT type, history, COUNT(*) as count FROM browsingHistory WHERE type = "{history_type}" GROUP BY type, history ORDER BY count DESC LIMIT {rank - 1}, 1;'
                cursor.execute(sql)
                history = cursor.fetchone()

                if history:
                    # Fetch details based on type
                    if history[0] == 'restaurant':
                        sql = f'SELECT id, name, photos FROM RestaurantData WHERE id = {history[1]};'
                    elif history[0] == 'attraction':
                        sql = f'SELECT id, name, photos FROM AttractionData WHERE id = {history[1]};'
                    elif history[0] == 'hotel':
                        sql = f'SELECT id, name, photos FROM HotelData WHERE id = {history[1]};'

                    cursor.execute(sql)
                    result = cursor.fetchone()

                    # Append formatted result to the output list
                    formatHottestHistory.append({
                        'type': history[0],
                        'id': result[0],
                        'name': result[1],
                        'photos': result[2],
                        'dataType': history[0]  # Use history type as dataType
                    })

        return True, formatHottestHistory
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


def checkHottestCity():
    data = {}

    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    try:
        sql = 'SELECT type, history, COUNT(*) as count FROM browsingHistory GROUP BY type, history ORDER BY count DESC;'
        cursor.execute(sql)
        hottest_city_data = cursor.fetchall()

        for history in hottest_city_data:
            if history[0] == 'restaurant':
                sql = f'SELECT formatted_address FROM RestaurantData WHERE id = {history[1]};'
                cursor.execute(sql)
                result = cursor.fetchone()
                address = result[0]
                for i in range(len(city)):
                    if city[i] in address:
                        city_name = city[i]
                        if city_name not in data:
                            data[city_name] = {
                                'labels': city_name,
                                'values': 0,
                                'lat': cityData[city_name]['latitude'],
                                'lng': cityData[city_name]['longitude'],
                                'photo': cityData[city_name]['photo']
                            }
                        data[city_name]['values'] += history[2]
                        break
            elif history[0] == 'attraction':
                sql = f'SELECT formatted_address FROM AttractionData WHERE id = {history[1]};'
                cursor.execute(sql)
                result = cursor.fetchone()
                address = result[0]
                for i in range(len(city)):
                    if city[i] in address:
                        city_name = city[i]
                        if city_name not in data:
                            data[city_name] = {
                                'labels': city_name,
                                'values': 0,
                                'lat': cityData[city_name]['latitude'],
                                'lng': cityData[city_name]['longitude'],
                                'photo': cityData[city_name]['photo']
                            }
                        data[city_name]['values'] += history[2]
                        break
            elif history[0] == 'hotel':
                sql = f'SELECT formatted_address FROM HotelData WHERE id = {history[1]};'
                cursor.execute(sql)
                result = cursor.fetchone()
                address = result[0]
                for i in range(len(city)):
                    if city[i] in address:
                        city_name = city[i]
                        if city_name not in data:
                            data[city_name] = {
                                'labels': city_name,
                                'values': 0,
                                'lat': cityData[city_name]['latitude'],
                                'lng': cityData[city_name]['longitude'],
                                'photo': cityData[city_name]['photo']
                            }
                        data[city_name]['values'] += history[2]
                        break

        # Sort the data by values in descending order
        sorted_data = sorted(data.values(), key=lambda x: x['values'], reverse=True)

        # Convert the data to the desired output format
        output_data = {item['labels']: item for item in sorted_data}
        return True, output_data

    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


def checkHottestSchedule(user_id):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    formatHottestSchedule = {}
    try:
        sql = 'SELECT s.userID, u.username, s.id, s.name, s.sDescribe, s.numberofLikes, s.timeStamp FROM schedule s JOIN User u ON s.userID = u.id WHERE s.privilege = 1 ORDER BY s.numberofLikes DESC;'
        cursor.execute(sql)
        hottestSchedule = cursor.fetchall()

        for schedule in hottestSchedule:
            schedule_id = schedule[2]
            sql = 'SELECT * FROM `likesHistory` WHERE user_id = %s AND schedule_id = %s;'
            value = (user_id, schedule_id)
            cursor.execute(sql, value)
            result = cursor.fetchone()
            if schedule_id not in formatHottestSchedule:
                formatHottestSchedule[schedule_id] = {
                    'scheduleID': schedule_id,
                    'name': schedule[3],
                    'Describe': schedule[4],
                    'numberofLikes': schedule[5],
                    'timeStamp': schedule[6].strftime('%Y-%m-%d'),
                    'userID': schedule[0],
                    'username': schedule[1],
                    'liked': True if result else False,
                    'trip': [],
                    'photos': []
                }

            sql = 'SELECT type, trip, startDate, endDate FROM trip WHERE scheduleID = %s ORDER BY startDate;'
            value = (schedule_id,)
            cursor.execute(sql, value)
            trips = cursor.fetchall()
            for trip in trips:
                if trip[0] == 'Restaurant':
                    sql = 'SELECT id, name, photos FROM RestaurantData WHERE id = %s;'
                    value = (trip[1],)
                    cursor.execute(sql, value)
                    result = cursor.fetchone()
                    if result:
                        formatHottestSchedule[schedule_id]['trip'].append(
                            {
                                'type': trip[0],
                                'id': result[0],
                                'name': result[1],
                                'startDate': trip[2],
                                'endDate': trip[3]
                            }
                        )
                        formatHottestSchedule[schedule_id]['photos'].append(result[2])
                    else:
                        pass
                elif trip[0] == 'Attraction':
                    sql = 'SELECT id, name, photos FROM AttractionData WHERE id = %s;'
                    value = (trip[1],)
                    cursor.execute(sql, value)
                    result = cursor.fetchone()
                    if result:
                        formatHottestSchedule[schedule_id]['trip'].append(
                            {
                                'type': trip[0],
                                'id': result[0],
                                'name': result[1],
                                'startDate': trip[2],
                                'endDate': trip[3]
                            }
                        )
                        formatHottestSchedule[schedule_id]['photos'].append(result[2])
                    else:
                        pass
                elif trip[0] == 'Hotel':
                    sql = 'SELECT id, name, photos FROM HotelData WHERE id = %s;'
                    value = (trip[1],)
                    cursor.execute(sql, value)
                    result = cursor.fetchone()
                    if result:
                        formatHottestSchedule[schedule_id]['trip'].append(
                            {
                                'type': trip[0],
                                'id': result[0],
                                'name': result[1],
                                'startDate': trip[2],
                                'endDate': trip[3]
                            }
                        )
                        formatHottestSchedule[schedule_id]['photos'].append(result[2])
                    else:
                        pass

    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()
        filtered_schedule = {k: v for k, v in formatHottestSchedule.items() if len(v['trip']) >= 4}
        return True, filtered_schedule


def likeSchedule(user_id, schedule_id):
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    try:
        sql = 'SELECT * FROM `likesHistory` WHERE user_id = %s AND schedule_id = %s;'
        value = (user_id, schedule_id)
        cursor.execute(sql, value)
        result = cursor.fetchone()
        if result:
            sql = 'DELETE FROM `likesHistory` WHERE user_id = %s AND schedule_id = %s;'
            value = (user_id, schedule_id)
            cursor.execute(sql, value)
            sql = 'UPDATE schedule SET numberofLikes = numberofLikes - 1 WHERE id = %s;'
            cursor.execute(sql, (schedule_id,))
            conn.commit()
            return True, '取消成功'
        else:
            sql = 'INSERT INTO `likesHistory` (user_id, schedule_id) VALUES (%s, %s);'
            value = (user_id, schedule_id)
            cursor.execute(sql, value)
            sql = 'UPDATE schedule SET numberofLikes = numberofLikes + 1 WHERE id = %s;'
            cursor.execute(sql, (schedule_id,))
            conn.commit()
            return True, '按讚成功'
    except mysql.connector.Error as err:
        return False, f"Error: {err}"
    finally:
        cursor.close()
        conn.close()


_news_cache = {"time": None, "data": []}


def getNews():
    """本月觀光活動（交通部觀光署 taiwan.net.tw）。

    2023 版以 Selenium 逐一抓取固定 XPath，網站改版後會逾時並回傳 500。
    該頁為伺服器端產生的 HTML，直接以 HTTP 取回並解析即可，並快取一小時；失敗時回傳空清單。
    """
    import html
    import re
    import urllib.request
    from urllib.parse import urljoin

    if _news_cache["time"] and datetime.now() - _news_cache["time"] < timedelta(hours=1):
        return True, _news_cache["data"]
    json_results = []
    try:
        # 獲取當天日期
        current_date = datetime.now().strftime("%Y%m%d")

        # 計算當月月底日期
        first_day_of_next_month = datetime.now().replace(day=28) + timedelta(days=4)
        last_day_of_month = first_day_of_next_month - timedelta(days=first_day_of_next_month.day)
        url = f"https://www.taiwan.net.tw/m1.aspx?sNo=0001019&keyString=^^^^{current_date}^{last_day_of_month.strftime('%Y%m%d')}"

        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        page = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="replace")
        block = page.split('class="columnBlock-list"', 1)[-1]
        for li in block.split("<li>")[1:]:
            img = re.search(r'data-src="([^"]+)"', li)
            link = re.search(r'<a href="([^"]+)" title="([^"]*)" class="columnBlock-title"', li)
            if not link:
                continue
            json_results.append({
                "title": html.unescape(link.group(2)).strip(),
                "photo": urljoin(url, html.unescape(img.group(1))) if img else None,
                "src": urljoin(url, html.unescape(link.group(1))),
            })
        _news_cache.update(time=datetime.now(), data=json_results)
    except Exception as e:
        print(f"getNews failed: {e}")
    return True, json_results
