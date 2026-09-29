"""Create a demo account (and fill in its questionnaire) through the API.

Usage:  python tools/create_demo_user.py [--base http://127.0.0.1:5000] [--username demo] [--password mitrip-demo]
"""
import argparse
import json
import urllib.error
import urllib.request


def call(base, method, path, body=None):
    req = urllib.request.Request(base + path, data=json.dumps(body).encode() if body is not None else None,
                                 method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:5000")
    ap.add_argument("--username", default="demo")
    ap.add_argument("--password", default="mitrip-demo")
    a = ap.parse_args()
    status, res = call(a.base, "POST", "/api/register", {"username": a.username, "password": a.password,
                                                         "email": f"{a.username}@example.com", "birthDay": "2001-01-01"})
    print("register:", status, res.get("message"))
    status, res = call(a.base, "POST", "/api/login", {"username": a.username, "password": a.password})
    token = res.get("token")
    status, res = call(a.base, "POST", "/api/user-information", {"token": token})
    uid = res["info"]["user_id"]
    status, res = call(a.base, "GET", f"/api/qes/isRecord/{uid}")
    if status != 200:  # no questionnaire yet
        call(a.base, "POST", "/api/qes/addRecord", {
            "userID": uid, "Age": "1", "Gender": "0", "Job": "0", "CityTravelDays": "0", "MtTravelType": "1",
            "PurchasedItem": "2", "TravelDays": "2", "TravelDaysBudget1": "1500", "TravelDaysBudget2": "3000",
            "TravelDaysBudget3": "6000", "TravelDaysBudget5": "9000", "TravelDaysBudget7": "12000", "TravelInfo": "2",
            "TravelMedia": "0", "TravelNeeds": "2", "TravelPeople": "1", "TravelSchedule": "1", "TravelType": "0"})
    print(f"demo user ready: username={a.username} password={a.password} user_id={uid}")


if __name__ == "__main__":
    main()
