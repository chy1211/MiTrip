"""Seed demo activity so the app does not look empty in a fresh database.

Creates (idempotently):
  * sample itineraries for the demo account (username `demo`)
  * a few fictional community users with public itineraries and likes ("熱門行程")
  * browsing history spread over several cities ("熱門城市" / "熱門商家")
It also removes the throw-away accounts created by tools/smoke_test.py (demo12345 ...).

All places are picked from the imported data: attractions by name, restaurants and hotels
automatically near the previous stop (highly rated, with a photo).

Usage:  python db/seed_demo.py
"""
import math
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

import mysql.connector
from werkzeug.security import generate_password_hash

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from config import MYSQL_CONFIG  # noqa: E402

DEMO_USER = ("demo", "mitrip-demo", "demo@example.com", "2001-01-01")
COMMUNITY = [  # fictional users; they never log in, so their passwords are random
    ("mei_travels", "mei@example.com", "1998-04-12"),
    ("ken_hualien", "ken@example.com", "1995-09-03"),
    ("amy_foodie", "amy@example.com", "2000-12-24"),
    ("joe_outdoors", "joe@example.com", "1993-06-18"),
    ("lin_weekend", "lin@example.com", "1999-02-27"),
]

# (owner, name, description, first day, public?, stops)
# stop = (day, "HH:MM", minutes, kind, arg): kind "A" = attraction by name,
#        "R" = restaurant near previous stop, "H" = hotel near previous stop
ITINERARIES = [
    ("demo", "高雄港灣兩天一夜", "駁二、西子灣看夕陽、旗津吹海風，第二天到蓮池潭散步", "2026-10-17", 1, [
        (1, "09:30", 120, "A", "駁二藝術特區"), (1, "12:00", 60, "R", None), (1, "13:30", 120, "A", "西子灣風景區"),
        (1, "16:00", 120, "A", "旗津海岸公園"), (1, "18:30", 90, "R", None), (1, "20:30", 720, "H", None),
        (2, "09:30", 90, "A", "蓮池潭風景區"), (2, "11:30", 60, "R", None)]),
    ("demo", "台北經典一日遊", "故宮、士林官邸到象山看夜景", "2026-11-07", 0, [
        (1, "09:30", 150, "A", "國立故宮博物院"), (1, "12:30", 60, "R", None), (1, "14:00", 90, "A", "士林官邸"),
        (1, "16:30", 90, "A", "象山"), (1, "18:30", 90, "R", None)]),
    ("demo", "新北山城老街", "十分放天燈、九份看山城夜景", "2026-11-21", 0, [
        (1, "09:30", 60, "A", "十分瀑布"), (1, "11:00", 90, "A", "十分老街"), (1, "12:30", 60, "R", None),
        (1, "15:00", 150, "A", "九份老街"), (1, "18:00", 90, "R", None)]),
    ("mei_travels", "台中文青散步", "審計新村逛小店、高美濕地等夕陽，晚上逢甲夜市", "2026-10-24", 1, [
        (1, "10:00", 120, "A", "審計368新創聚落(審計新村)"), (1, "12:30", 60, "R", None), (1, "15:30", 150, "A", "高美濕地"),
        (1, "19:00", 120, "A", "逢甲夜市"), (1, "21:30", 720, "H", None)]),
    ("ken_hualien", "花蓮海岸兩日遊", "七星潭、清水斷崖與太魯閣", "2026-11-14", 1, [
        (1, "10:00", 90, "A", "七星潭海岸風景特定區"), (1, "12:00", 60, "R", None), (1, "14:00", 60, "A", "清水斷崖景觀台"),
        (1, "18:00", 720, "H", None), (2, "09:00", 150, "A", "太魯閣台地步道"), (2, "12:00", 60, "R", None)]),
    ("amy_foodie", "台南古都小吃巡禮", "赤崁樓、神農街、林百貨，一路吃到安平", "2026-10-31", 1, [
        (1, "09:30", 60, "A", "赤崁樓"), (1, "10:45", 45, "R", None), (1, "12:00", 60, "A", "台南林百貨"),
        (1, "13:30", 60, "R", None), (1, "15:00", 90, "A", "安平古堡"), (1, "18:00", 90, "A", "神農街"), (1, "19:45", 60, "R", None)]),
    ("joe_outdoors", "日月潭環湖兩日", "搭纜車看日月潭、文武廟，隔天向山看湖景再到埔里", "2026-12-05", 1, [
        (1, "10:00", 120, "A", "日月潭纜車站"), (1, "12:30", 60, "R", None), (1, "14:00", 90, "A", "日月潭文武廟"),
        (1, "16:00", 60, "A", "水社碼頭"), (1, "18:00", 720, "H", None),
        (2, "09:30", 90, "A", "向山懸臂式觀景台"), (2, "12:30", 60, "A", "埔里酒廠展售中心"), (2, "13:45", 60, "R", None)]),
    ("lin_weekend", "淡水北投溫泉散策", "北投泡湯看溫泉博物館，傍晚到淡水", "2026-12-12", 1, [
        (1, "10:00", 90, "A", "北投溫泉博物館"), (1, "11:45", 45, "A", "北投公園"), (1, "12:45", 60, "R", None),
        (1, "15:00", 90, "A", "淡水紅毛城"), (1, "17:00", 120, "A", "淡水老街"), (1, "19:15", 60, "R", None)]),
]
# schedule name -> users who liked it
LIKES = {
    "高雄港灣兩天一夜": ["mei_travels", "ken_hualien", "amy_foodie", "lin_weekend"],
    "台中文青散步": ["demo", "amy_foodie", "joe_outdoors", "lin_weekend", "ken_hualien"],
    "花蓮海岸兩日遊": ["joe_outdoors", "mei_travels", "lin_weekend"],
    "台南古都小吃巡禮": ["demo", "mei_travels", "ken_hualien", "joe_outdoors", "lin_weekend"],
    "日月潭環湖兩日": ["ken_hualien", "amy_foodie"],
    "淡水北投溫泉散策": ["demo", "mei_travels"],
}
# city -> relative popularity used to generate browsing history
CITY_VIEWS = {"台北市": 60, "高雄市": 48, "台南市": 40, "台中市": 34, "新北市": 28, "花蓮縣": 20,
              "南投縣": 16, "嘉義市": 12, "屏東縣": 10, "宜蘭縣": 8}


def km(a, b):
    p = math.pi / 180
    h = 0.5 - math.cos((b[0] - a[0]) * p) / 2 + math.cos(a[0] * p) * math.cos(b[0] * p) * (1 - math.cos((b[1] - a[1]) * p)) / 2
    return 12742 * math.asin(math.sqrt(h))


def drive_minutes(a, b):  # same estimate as backend/tools/distanceNtime.py
    d = km(a, b) * 1.3
    return max(5, round(d / (25 if d < 5 else 40) * 60))


def find_attraction(cur, name):
    cur.execute("SELECT id, lat, lng FROM AttractionData WHERE name = %s ORDER BY user_ratings_total DESC LIMIT 1", (name,))
    row = cur.fetchone()
    if not row:
        cur.execute("SELECT id, lat, lng FROM AttractionData WHERE name LIKE %s ORDER BY user_ratings_total DESC LIMIT 1", (f"%{name}%",))
        row = cur.fetchone()
    if not row:
        raise SystemExit(f"attraction not found: {name}")
    return row


def find_near(cur, table, lat, lng, used, radius_km, strict=True):
    """Best-reviewed place near (lat, lng); widen the radius, then relax the filters, if nothing matches."""
    d = radius_km / 111
    filters = "AND photos IS NOT NULL AND rating >= 4.0 AND user_ratings_total >= 50" if strict else "AND rating >= 3.5"
    if strict and table == "RestaurantData":
        filters += " AND class IS NOT NULL"
    cur.execute(f"""SELECT id, lat, lng, user_ratings_total FROM {table}
                    WHERE lat BETWEEN %s AND %s AND lng BETWEEN %s AND %s {filters}
                    ORDER BY user_ratings_total DESC LIMIT 60""", (lat - d, lat + d, lng - d, lng + d))
    for row in cur.fetchall():
        if row[0] not in used and km((lat, lng), (row[1], row[2])) <= radius_km:
            return row[:3]
    if radius_km < 12:
        return find_near(cur, table, lat, lng, used, radius_km * 2, strict)
    if strict:
        return find_near(cur, table, lat, lng, used, 3, strict=False)
    raise SystemExit(f"no {table} near {lat},{lng}")


def ensure_user(cur, username, email, birthday, password=None):
    cur.execute("SELECT id FROM User WHERE username = %s", (username,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO User (username, password, email, birthDay) VALUES (%s, %s, %s, %s)",
                (username, generate_password_hash(password or random.randbytes(16).hex()), email, birthday))
    return cur.lastrowid


def delete_user_activity(cur, user_ids):
    if not user_ids:
        return
    ph = ", ".join(["%s"] * len(user_ids))
    cur.execute(f"SELECT id FROM schedule WHERE userID IN ({ph})", user_ids)
    sids = [r[0] for r in cur.fetchall()]
    if sids:
        sp = ", ".join(["%s"] * len(sids))
        cur.execute(f"DELETE FROM trip WHERE scheduleID IN ({sp})", sids)
        cur.execute(f"DELETE FROM likesHistory WHERE schedule_id IN ({sp})", sids)
        cur.execute(f"DELETE FROM schedule WHERE id IN ({sp})", sids)
    cur.execute(f"DELETE FROM likesHistory WHERE user_id IN ({ph})", user_ids)
    cur.execute(f"DELETE FROM browsingHistory WHERE userID IN ({ph})", user_ids)


def main():
    random.seed(20231208)
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cur = conn.cursor()

    # 1) drop throw-away smoke-test accounts
    cur.execute("SELECT id FROM User WHERE username REGEXP '^demo[0-9]+$'")
    smoke = [r[0] for r in cur.fetchall()]
    delete_user_activity(cur, smoke)
    if smoke:
        ph = ", ".join(["%s"] * len(smoke))
        for t, col in (("Token", "user_id"), ("userPreferences", "userID"), ("RestaurantReviews", "userID"),
                       ("AttractionReviews", "userID"), ("HotelReviews", "userID"), ("User", "id")):
            cur.execute(f"DELETE FROM {t} WHERE {col} IN ({ph})", smoke)

    # 2) users
    users = {"demo": ensure_user(cur, *DEMO_USER[:1], DEMO_USER[2], DEMO_USER[3], password=DEMO_USER[1])}
    for name, email, bday in COMMUNITY:
        users[name] = ensure_user(cur, name, email, bday)
    delete_user_activity(cur, list(users.values()))

    # 3) itineraries
    schedule_ids = {}
    for owner, name, desc, first_day, public, stops in ITINERARIES:
        day0 = datetime.strptime(first_day, "%Y-%m-%d")
        last_day = max(s[0] for s in stops)
        cur.execute("INSERT INTO schedule (name, sDescribe, startDate, endDate, userID, privilege, timeStamp) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, desc, day0 + timedelta(hours=9), day0 + timedelta(days=last_day - 1, hours=21), users[owner], public,
                     datetime.now() - timedelta(days=random.randint(1, 20))))
        sid = cur.lastrowid
        schedule_ids[name] = sid
        used, placed, prev = set(), [], None
        for day, hhmm, minutes, kind, arg in stops:
            if kind == "A":
                pid, lat, lng = find_attraction(cur, arg)
                ttype = "Attraction"
            else:
                table, ttype, radius = ("RestaurantData", "Restaurant", 1.5) if kind == "R" else ("HotelData", "Hotel", 3)
                pid, lat, lng = find_near(cur, table, prev[0], prev[1], used, radius)
            used.add(pid)
            start = day0 + timedelta(days=day - 1, hours=int(hhmm[:2]), minutes=int(hhmm[3:]))
            placed.append([ttype, pid, start, start + timedelta(minutes=minutes), (float(lat), float(lng)), day])
            prev = (float(lat), float(lng))
        for i, (ttype, pid, start, end, pos, day) in enumerate(placed):
            nxt = placed[i + 1] if i + 1 < len(placed) and placed[i + 1][5] == day else None
            h, m = divmod(drive_minutes(pos, nxt[4]), 60) if nxt else (None, None)
            cur.execute("INSERT INTO trip (scheduleID, type, trip, startDate, endDate, userID, nextHours, nextMinutes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (sid, ttype, pid, start, end, users[owner], h, m))

    # 4) likes
    for name, likers in LIKES.items():
        for u in likers:
            cur.execute("INSERT INTO likesHistory (user_id, schedule_id) VALUES (%s, %s)", (users[u], schedule_ids[name]))
        cur.execute("UPDATE schedule SET numberofLikes = %s WHERE id = %s", (len(likers), schedule_ids[name]))

    # 5) browsing history spread over cities (restaurants / hotels / attractions with photos)
    viewers = list(users.values())
    rows = []
    for city, weight in CITY_VIEWS.items():
        for table, htype, n in (("RestaurantData", "restaurant", 6), ("AttractionData", "attraction", 4), ("HotelData", "hotel", 3)):
            cur.execute(f"SELECT id FROM {table} WHERE formatted_address LIKE %s AND photos IS NOT NULL AND user_ratings_total >= 100 "
                        f"ORDER BY user_ratings_total DESC LIMIT %s", (f"%{city}%", n))
            for rank, (pid,) in enumerate(cur.fetchall()):
                for _ in range(max(1, weight // (rank + 2))):
                    rows.append((random.choice(viewers), htype, pid, datetime.now() - timedelta(days=random.randint(0, 30), minutes=random.randint(0, 1440))))
    cur.executemany("INSERT INTO browsingHistory (userID, type, history, time) VALUES (%s, %s, %s, %s)", rows)

    conn.commit()
    cur.execute("SELECT COUNT(*) FROM trip WHERE scheduleID IN (%s)" % ", ".join(str(s) for s in schedule_ids.values()))
    print(f"removed smoke-test users: {len(smoke)}")
    print(f"itineraries: {len(schedule_ids)} (trips: {cur.fetchone()[0]}), likes: {sum(len(v) for v in LIKES.values())}, browsing rows: {len(rows)}")
    print(f"demo login: {DEMO_USER[0]} / {DEMO_USER[1]}")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
