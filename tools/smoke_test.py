"""End-to-end smoke test for the MiTrip API (backend must be running).

Walks one user through: register -> login -> questionnaire -> recommendations -> detail -> search
-> schedule + trips -> travel time -> reviews -> explore.

Usage:  python tools/smoke_test.py [--base http://127.0.0.1:5000]
"""
import argparse
import json
import time
import urllib.error
import urllib.request

LAT, LNG = 22.774424, 120.399112  # NKUST Yanchao campus, the default location used by the app


class Api:
    def __init__(self, base):
        self.base = base.rstrip("/")
        self.results = []

    def call(self, method, path, body=None, expect=(200, 201)):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method,
                                     headers={"Content-Type": "application/json"})
        t = time.time()
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                status, raw = r.status, r.read()
        except urllib.error.HTTPError as e:
            status, raw = e.code, e.read()
        ms = int((time.time() - t) * 1000)
        try:
            payload = json.loads(raw)
        except ValueError:
            payload = raw.decode(errors="replace")
        ok = status in expect
        self.results.append((ok, method, path.split("?")[0], status, ms, summarize(payload)))
        return payload


def summarize(p):
    if isinstance(p, list):
        return f"list[{len(p)}]"
    if isinstance(p, dict):
        for k in ("message", "success"):
            if k in p and not isinstance(p[k], (list, dict)):
                return f"{k}={str(p[k])[:40]}"
        return f"dict[{len(p)}]"
    return str(p)[:50]


def first_id(payload):
    """Recommendation endpoints return {"0": {...}, "1": {...}} or a list."""
    items = payload.values() if isinstance(payload, dict) else payload
    for it in items:
        if isinstance(it, dict) and "id" in it:
            return it["id"]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:5000")
    api = Api(ap.parse_args().base)
    user = f"demo{int(time.time()) % 100000}"

    api.call("POST", "/api/register", {"username": user, "password": "demo-pass-123", "email": f"{user}@example.com", "birthDay": "2001-01-01"})
    token = api.call("POST", "/api/login", {"username": user, "password": "demo-pass-123"}).get("token")
    info = api.call("POST", "/api/user-information", {"token": token})
    uid = (info.get("info") or {}).get("user_id") if isinstance(info, dict) else None

    api.call("GET", f"/api/qes/isRecord/{uid}")
    api.call("POST", "/api/qes/addRecord", {
        "userID": uid, "Age": "1", "Gender": "0", "Job": "0", "CityTravelDays": "0", "MtTravelType": "1",
        "PurchasedItem": "2", "TravelDays": "2", "TravelDaysBudget1": "1500", "TravelDaysBudget2": "3000",
        "TravelDaysBudget3": "6000", "TravelDaysBudget5": "9000", "TravelDaysBudget7": "12000", "TravelInfo": "2",
        "TravelMedia": "0", "TravelNeeds": "2", "TravelPeople": "1", "TravelSchedule": "1", "TravelType": "0"})

    ids = {}
    for kind in ("restaurant", "attraction", "hotel"):
        rec = api.call("GET", f"/api/{kind}?user_id={uid}&lat={LAT}&lng={LNG}")
        ids[kind] = first_id(rec)
        if ids[kind]:
            api.call("GET", f"/api/{kind}/{ids[kind]}?user_id={uid}")
            api.call("GET", f"/api/{kind}/{ids[kind]}/reviews")
    api.call("GET", f"/api/restaurant/search?keyWord=%E9%BA%B5&lat={LAT}&lng={LNG}")  # "麵"

    api.call("POST", "/api/schedule/insert_data", {"name": "Demo trip", "sDescribe": "smoke test", "startDate": "2026-10-10 09:00:00",
                                                  "endDate": "2026-10-11 20:00:00", "userID": uid, "privilege": 1})
    schedules = api.call("GET", f"/api/schedule/select_by_user_id/{uid}")
    sid = next(iter(schedules.values()))["scheduleID"] if isinstance(schedules, dict) and schedules else None
    for kind, tid in (("Attraction", ids.get("attraction")), ("Restaurant", ids.get("restaurant"))):
        if sid and tid:
            api.call("POST", "/api/trips", {"scheduleID": sid, "trip_type": kind, "trip_id": tid, "user_id": uid})
    detail = api.call("GET", f"/api/schedule/select_by_id/{sid}")
    trips = [t for t in (detail if isinstance(detail, list) else []) if isinstance(t, dict) and t.get("tripID")]
    if len(trips) >= 2:
        a, b = trips[0], trips[1]
        api.call("POST", "/api/get_distance_and_time", {
            "aID": a["tripID"], "aType": a["tripType"], "aTrip": a.get("attractionID") or a.get("restaurantID"),
            "bID": b["tripID"], "bType": b["tripType"], "bTrip": b.get("restaurantID") or b.get("attractionID"),
            "end_date": a["tripEndDate"], "b_durationH": 1, "b_drurationM": 0})
        # drag-and-drop: swap the two stops and let the backend re-time the itinerary
        api.call("POST", f"/api/schedule/{sid}/reflow", {"order": [{"tripID": b["tripID"], "day": 1}, {"tripID": a["tripID"], "day": 1}]})

    if ids.get("restaurant"):
        api.call("POST", "/api/restaurant/addReview", {"restaurantId": ids["restaurant"], "userId": uid, "text": "smoke test review", "userRating": 4})
        api.call("GET", f"/api/restaurant/userID/{uid}/reviews")
    api.call("GET", "/api/explore/checkHottestCity")
    api.call("GET", "/api/explore/checkHottestHistory")
    api.call("GET", f"/api/explore/checkHottestSchedule?user_id={uid}")
    api.call("GET", "/api/explore/get_news")

    width = max(len(r[2]) for r in api.results)
    for ok, m, p, s, ms, summ in api.results:
        print(f"{'PASS' if ok else 'FAIL'}  {m:6s} {p:{width}s}  {s}  {ms:6d} ms  {summ}")
    fails = sum(not r[0] for r in api.results)
    print(f"\n{len(api.results) - fails}/{len(api.results)} passed  (user={user}, id={uid})")
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
