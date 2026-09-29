import os
import pandas as pd
import time
import googlemaps

api_key = os.environ["GOOGLE_MAPS_API_KEY"]
gmaps = googlemaps.Client(key=api_key)
df_g = pd.read_csv("Hotel-gt.csv", usecols=["Name"])

# Set search parameters
business_type = "lodging"  # Business type as lodging

# Create an empty list to store the results
results = []

# Send API requests to get lodging data for each hotel name
ids = []
print("Start searching for lodging data...")
for name in df_g["Name"]:
    response = gmaps.places(query=name, type=business_type)
    print(f"Found {len(response['results'])} results for {name}")
    results.extend(response["results"])
    while "next_page_token" in response:
        time.sleep(
            2
        )  # Pause 2 seconds after each request to avoid exceeding API limits
        response = gmaps.places(
            query=name, type=business_type, page_token=response["next_page_token"]
        )
        results.extend(response["results"])
    for result in response["results"]:
        ids.append(result["place_id"])
    stores_info = []  # 儲存所有店家資訊
    ids = list(set(ids))  # 去除重複id
    for id in ids:
        stores_info.append(
            gmaps.place(place_id=id, language="zh-TW")["result"]
        )  # 取得店家資訊
    results += stores_info
    ids = []
print("Finished searching for lodging data.")

# Write the results to a CSV file
df = pd.DataFrame(results)

df.to_csv("hotel1.csv", encoding="utf-8-sig", index=False)
