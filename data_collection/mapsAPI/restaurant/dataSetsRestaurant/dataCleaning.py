import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd
from tqdm import tqdm

filePath = f"{DATA_DIR}/googlemap_restaurant.csv"
data = pd.read_csv(filePath, encoding="utf-8-sig")

# drop useless columns ["business_status", "current_opening_hours", "icon", "icon_background_color", "icon_mask_base_uri", "utc_offset", "editorial_summary"]
data = data.drop(
    columns=[
        "business_status",
        "current_opening_hours",
        "icon",
        "icon_background_color",
        "icon_mask_base_uri",
        "utc_offset",
        "editorial_summary",
    ]
)


# drop rows if "permanently_closed" == True
data = data[data["permanently_closed"] != "TRUE"]
print(data.shape)

# turn ["dine_in", "takeout"] into boolen
data["dine_in"] = data["dine_in"].astype(str)
data["takeout"] = data["takeout"].astype(str)
for i in tqdm(range(0, len(data["dine_in"]))):
    if data["dine_in"][i] == "True":
        data["dine_in"][i] = True
    else:
        data["dine_in"][i] = False
for i in tqdm(range(0, len(data["takeout"]))):
    if data["takeout"][i] == "True":
        data["takeout"][i] = True
    else:
        data["takeout"][i] = False


# trun reviews into string
data["reviews"] = data["reviews"].astype(str)

# convert to dict
reviews = data["reviews"]
dictReviews = []
for i in tqdm(range(0, len(reviews))):
    try:
        review = eval(reviews[i].replace("[", "").replace("]", ""))
        dictReviews.append(review)
    except Exception:
        # print(e)
        dictReviews.append(reviews[i])
        pass


# drop useless columns ["reviews", "permanently_closed"]
data = data.drop(columns=["reviews", "permanently_closed"])


# extract text from dict then save to csv
data["textReview"] = ""
Temp = []
for i in tqdm(range(0, len(dictReviews))):
    if type(dictReviews[i]) == str:
        data["textReview"][i] = dictReviews[i]
    else:
        for j in range(0, len(dictReviews[i])):
            try:
                text = dictReviews[i][j]["text"]
                Temp.append(text)
            except Exception:
                # print(e)
                data["textReview"][i] = dictReviews[i]["text"]
        data["textReview"][i] = Temp
        Temp = []
data["textReview"] = data["textReview"].astype(str)

# check if there is any row with empty textReview then trun them into "nan"
print(data[data["textReview"] == "[]"].shape)
data["textReview"] = data["textReview"].replace("[]", "nan")

# trun textReview into list them check if first item is empty, if so, trun it into "nan"
for i in tqdm(range(0, len(data["textReview"]))):
    if data["textReview"][i] != "nan":
        data["textReview"][i] = (
            data["textReview"][i]
            .replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .split(", ")
        )
        if data["textReview"][i][0] == "":
            data["textReview"][i] = "nan"
data["textReview"] = data["textReview"].astype(str)


# "department_store", "laundry", "lodging", "travel_agency",
# "shopping_mall", "school", "finance", "gas_station",
# "place_of_worship", "hospital", "spa", "pet_store",
# "movie_theater", "real_estate_agency"
# drop rows if ["types"] contains any of the above

data = data[
    ~data["types"].astype(str).str.contains("department_store")
    & ~data["types"].astype(str).str.contains("laundry")
    & ~data["types"].astype(str).str.contains("lodging")
    & ~data["types"].astype(str).str.contains("travel_agency")
    & ~data["types"].astype(str).str.contains("shopping_mall")
    & ~data["types"].astype(str).str.contains("school")
    & ~data["types"].astype(str).str.contains("finance")
    & ~data["types"].astype(str).str.contains("gas_station")
    & ~data["types"].astype(str).str.contains("place_of_worship")
    & ~data["types"].astype(str).str.contains("hospital")
    & ~data["types"].astype(str).str.contains("spa")
    & ~data["types"].astype(str).str.contains("pet_store")
    & ~data["types"].astype(str).str.contains("movie_theater")
    & ~data["types"].astype(str).str.contains("real_estate_agency")
]

# fill rating with 0 if pd.isna() == True
j = 0
for i in data["rating"]:
    if pd.isna(i):
        data["rating"][j] = 0
    j += 1
data["rating"] = data["rating"].astype(float)

# save to csv
data.to_csv(
    f"{DATA_DIR}/googleMap_restaurantWithTextReviews.csv",
    index=False,
    encoding="utf-8-sig",
)
