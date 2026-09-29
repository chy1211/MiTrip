"""Load MiTrip place data into MySQL.

The original 2023 database dump was not kept, so this script rebuilds the data tables
from the raw collection files:

  data_local/restaurant_outputClass.csv   Google Places restaurants (+ cuisine class, photo URL)
  data_local/hotels.csv                   Google Places lodging
  data_local/Hotel-GovData.csv            Taiwan Tourism Administration open data (lodging)
  data_local/filtered_tourist.csv         Google Places tourist attractions
  data_local/attraction_GovData_class.csv Taiwan Tourism Administration open data (attractions, labelled)
  data_local/qesData/questionnaire_encoded.csv  anonymised one-hot questionnaire answers (seed users)

Google Places content may not be redistributed, so data_local/ is git-ignored.

Usage:  python db/load_data.py [--limit N]
"""
import argparse
import ast
import csv
import difflib
import json
import math
import os
import sys
from pathlib import Path

import mysql.connector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from config import MYSQL_CONFIG  # noqa: E402

DATA = ROOT / "data_local"
csv.field_size_limit(10**9)
SEED_USER_BASE = 900000  # questionnaire respondents become userPreferences rows with userID 900001..

HOTEL_TYPES = ["帳篷", "度假飯店", "民宿", "背包客棧", "膠囊旅館", "酒店", "青年旅館", "飯店"]
ATTRACTION_TYPES = ["文化景點", "自然景點", "期間活動", "休閒娛樂", "娛樂演出"]


def lit(v):
    """Parse a Python-literal cell (the collectors wrote dict/list reprs)."""
    if v is None or v.strip() in ("", "None", "nan"):
        return None
    try:
        return ast.literal_eval(v)
    except (ValueError, SyntaxError):
        try:
            return json.loads(v)
        except ValueError:
            return None


def fnum(v, cast=float):
    try:
        x = cast(float(v))
        return None if isinstance(x, float) and math.isnan(x) else x
    except (TypeError, ValueError):
        return None


def flag(v):
    return v if v in ("True", "False") else None


def jdump(obj):
    return None if obj is None else json.dumps(obj, ensure_ascii=False)


def latlng(row):
    lat, lng = fnum(row.get("lat")), fnum(row.get("lng"))
    if lat is None or lng is None:
        g = lit(row.get("geometry", ""))
        if g:
            lat, lng = g["location"]["lat"], g["location"]["lng"]
    return lat, lng


def rows(name, limit=None):
    with open(DATA / name, encoding="utf-8-sig", newline="") as f:
        for i, r in enumerate(csv.DictReader(f)):
            if limit and i >= limit:
                break
            yield r


class GovIndex:
    """Grid index over government open-data records for nearest-name matching."""

    def __init__(self, records, lat_key, lng_key):
        self.cells = {}
        for r in records:
            lat, lng = fnum(r.get(lat_key)), fnum(r.get(lng_key))
            if lat is None or lng is None:
                continue
            r["_lat"], r["_lng"] = lat, lng
            self.cells.setdefault((round(lat, 2), round(lng, 2)), []).append(r)

    def match(self, name, lat, lng):
        best, best_score = None, 0.0
        for dlat in (-0.01, 0, 0.01):
            for dlng in (-0.01, 0, 0.01):
                for r in self.cells.get((round(lat + dlat, 2), round(lng + dlng, 2)), []):
                    d = haversine_m(lat, lng, r["_lat"], r["_lng"])
                    if d > 500:
                        continue
                    sim = difflib.SequenceMatcher(None, name, r.get("Name", "")).ratio()
                    score = sim + (0.5 if d < 100 else 0.25 if d < 250 else 0)
                    if (d < 150 or sim > 0.5) and score > best_score:
                        best, best_score = r, score
        return best


def haversine_m(lat1, lng1, lat2, lng2):
    p = math.pi / 180
    a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lng2 - lng1) * p)) / 2
    return 12742000 * math.asin(math.sqrt(a))


def hotel_class(name, types, gov):
    n = name.lower()
    if "露營" in name or "營地" in name or "campground" in types:
        return "帳篷"
    if "青年旅" in name or "青旅" in name or "hostel" in n:
        return "青年旅館"
    if "背包" in name or "backpack" in n:
        return "背包客棧"
    if "膠囊" in name or "capsule" in n:
        return "膠囊旅館"
    if "度假" in name or "渡假" in name or "resort" in n:
        return "度假飯店"
    if "民宿" in name or (gov and gov.get("Class") == "4"):
        return "民宿"
    if "酒店" in name:
        return "酒店"
    return "飯店"


def attraction_class(name, types):
    t = set(types or [])
    if t & {"amusement_park", "zoo", "aquarium", "shopping_mall", "stadium", "bowling_alley", "spa"} or any(k in name for k in ("樂園", "遊樂", "夜市", "商圈", "購物", "牧場", "農場")):
        return "休閒娛樂"
    if t & {"movie_theater", "night_club"} or any(k in name for k in ("劇場", "音樂廳", "表演", "藝術中心")):
        return "娛樂演出"
    if t & {"museum", "art_gallery", "place_of_worship", "church", "hindu_temple", "library"} or any(k in name for k in ("廟", "宮", "寺", "祠", "古蹟", "老街", "博物館", "紀念館", "文化", "故居")):
        return "文化景點"
    return "自然景點"


def load_restaurants(cur, limit):
    sql = """INSERT INTO RestaurantData (place_id, name, formatted_address, formatted_phone_number, opening_hours, url, website,
             rating, user_ratings_total, price_level, class, photos, lat, lng, wheelchair_accessible_entrance, serves_breakfast,
             serves_brunch, serves_lunch, serves_dinner, serves_beer, serves_wine, serves_vegetarian_food, curbside_pickup,
             takeout, delivery, reservable) VALUES (%s)""" % ", ".join(["%s"] * 26)
    seen, batch, n = set(), [], 0
    for r in rows("restaurant_outputClass.csv", limit):
        pid = r.get("place_id")
        lat, lng = latlng(r)
        if not r.get("name") or lat is None or pid in seen:
            continue
        seen.add(pid)
        cls = lit(r.get("class", ""))
        photo = r.get("photos") if (r.get("photos") or "").startswith("http") else None
        batch.append((pid, r["name"], r.get("formatted_address") or None, r.get("formatted_phone_number") or None,
                      jdump(lit(r.get("opening_hours", ""))), r.get("url") or None, r.get("website") or None,
                      fnum(r.get("rating")), fnum(r.get("user_ratings_total"), int), fnum(r.get("price_level"), int),
                      jdump(cls if isinstance(cls, list) and cls else None), photo, lat, lng,
                      flag(r.get("wheelchair_accessible_entrance")), flag(r.get("serves_breakfast")), flag(r.get("serves_brunch")),
                      flag(r.get("serves_lunch")), flag(r.get("serves_dinner")), flag(r.get("serves_beer")), flag(r.get("serves_wine")),
                      flag(r.get("serves_vegetarian_food")), flag(r.get("curbside_pickup")), flag(r.get("takeout")),
                      flag(r.get("delivery")), flag(r.get("reservable"))))
        if len(batch) >= 2000:
            cur.executemany(sql, batch); n += len(batch); batch = []
    if batch:
        cur.executemany(sql, batch); n += len(batch)
    return n


def load_hotels(cur, limit):
    gov = GovIndex(list(rows("Hotel-GovData.csv")), "Py", "Px")
    sql = """INSERT INTO HotelData (place_id, name, formatted_address, description, formatted_phone_number, website, opening_hours,
             url, rating, user_ratings_total, class, numberofRooms, lowestPrice, ceilingPrice, photos, lat, lng)
             VALUES (%s)""" % ", ".join(["%s"] * 17)
    seen, batch, matched = set(), [], 0
    for r in rows("hotels.csv", limit):
        pid = r.get("place_id")
        lat, lng = latlng(r)
        if not r.get("name") or lat is None or pid in seen or r.get("business_status") not in ("OPERATIONAL", ""):
            continue
        seen.add(pid)
        types = lit(r.get("types", "")) or []
        g = gov.match(r["name"], lat, lng)
        matched += g is not None
        batch.append((pid, r["name"], r.get("formatted_address") or None, (g or {}).get("Description") or None,
                      r.get("formatted_phone_number") or None, r.get("website") or None, jdump(lit(r.get("opening_hours", ""))),
                      r.get("url") or None, fnum(r.get("rating")), fnum(r.get("user_ratings_total"), int),
                      jdump({"class": hotel_class(r["name"], types, g)}),
                      fnum((g or {}).get("TotalNumberofRooms"), int), fnum((g or {}).get("LowestPrice"), int),
                      fnum((g or {}).get("CeilingPrice"), int), (g or {}).get("Picture1") or None, lat, lng))
    cur.executemany(sql, batch)
    return len(batch), matched


def load_attractions(cur, limit):
    gov = GovIndex(list(rows("attraction_GovData_class.csv")), "Py", "Px")
    sql = """INSERT INTO AttractionData (place_id, name, formatted_address, formatted_phone_number, opening_hours, url, website,
             rating, user_ratings_total, class, photos, description, lat, lng) VALUES (%s)""" % ", ".join(["%s"] * 14)
    seen, batch, matched = set(), [], 0
    for r in rows("filtered_tourist.csv", limit):
        pid = r.get("place_id")
        lat, lng = latlng(r)
        if not r.get("name") or lat is None or pid in seen or r.get("business_status") not in ("OPERATIONAL", ""):
            continue
        seen.add(pid)
        types = lit(r.get("types", "")) or []
        g = gov.match(r["name"], lat, lng)
        matched += g is not None
        cls = g["class"] if g and g.get("class") in ATTRACTION_TYPES else attraction_class(r["name"], types)
        batch.append((pid, r["name"], r.get("formatted_address") or None, r.get("formatted_phone_number") or None,
                      jdump(lit(r.get("opening_hours", ""))), r.get("url") or f"https://www.google.com/maps/place/?q=place_id:{pid}",
                      r.get("website") or None, fnum(r.get("rating")), fnum(r.get("user_ratings_total"), int), jdump([cls]),
                      (g or {}).get("Picture1") or None, (g or {}).get("Toldescribe") or (g or {}).get("Description") or None, lat, lng))
    cur.executemany(sql, batch)
    return len(batch), matched


def load_seed_preferences(cur):
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = 'userPreferences'")
    table_cols = {c[0] for c in cur.fetchall()}
    with open(DATA / "qesData" / "questionnaire_encoded.csv", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        keep = [i for i, c in enumerate(header) if c in table_cols]
        cols = ", ".join(f"`{header[i]}`" for i in keep)
        sql = f"INSERT INTO userPreferences (userID, {cols}) VALUES (%s, {', '.join(['%s'] * len(keep))})"
        batch = [(SEED_USER_BASE + n + 1, *[fnum(row[i]) or 0 for i in keep]) for n, row in enumerate(reader)]
    cur.executemany(sql, batch)
    return len(batch)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="only read the first N rows of each place file")
    args = ap.parse_args()
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cur = conn.cursor()
    for t in ("RestaurantData", "HotelData", "AttractionData"):
        cur.execute(f"TRUNCATE TABLE `{t}`")
    cur.execute("DELETE FROM userPreferences WHERE userID > %s", (SEED_USER_BASE,))
    print("restaurants:", load_restaurants(cur, args.limit)); conn.commit()
    print("hotels (rows, matched to open data):", load_hotels(cur, args.limit)); conn.commit()
    print("attractions (rows, matched to open data):", load_attractions(cur, args.limit)); conn.commit()
    print("seed questionnaire users:", load_seed_preferences(cur)); conn.commit()
    cur.close(); conn.close()


if __name__ == "__main__":
    main()
