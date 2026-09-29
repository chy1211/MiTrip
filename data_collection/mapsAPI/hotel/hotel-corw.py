import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd
import time
import googlemaps

api_key = os.environ["GOOGLE_MAPS_API_KEY"]
gmaps = googlemaps.Client(key=api_key)
df_g = pd.read_csv("Hotel-g.csv", usecols=["Name"])
print(df_g.head())

# Set search parameters
type = "lodging"  # Business type as lodging

# Set API key and API URL

url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Create an empty list to store the results
results = []

# Send API requests to get lodging data for each hotel name
print("Start searching for lodging data...")
for name in df_g["Name"]:
    response = gmaps.places(query=name, type="lodging")
    print(f"Found {len(response)} results")
    print(response)
    results += response
    time.sleep(2)  # Pause 2 seconds after each request to avoid exceeding API limits

# Convert the results to a DataFrame
df = pd.DataFrame(results)
df.to_csv(
    f"{DATA_DIR}/result/googlemap_hotel.csv", index=False,
)
