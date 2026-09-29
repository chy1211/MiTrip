import os
DATA_DIR = os.getenv("MITRIP_DATA_DIR", "data_local")  # raw/offline data folder
import pandas as pd

filePath = f"{DATA_DIR}/googleMap_restaurantWithTextReviews.csv"
data = pd.read_csv(filePath)

name = data["name"]
reviews = data["textReview"]
print(reviews[0])
print(type(reviews[0]))

print(reviews[1])
print(type(reviews[1]))
list = reviews[1].replace("['", "").replace("']", "").split("', '")
print(list)
print(type(list))


# for i in range(len(reviews)):
#     if reviews[i] == "nan":
#         print("No reviews")
#     else:
#         print(reviews[i])

# for i in range(len(reviews)):
#     print(name[i], ":", reviews[i])
#     print(len(list(reviews[i])))
#     print("\n")
