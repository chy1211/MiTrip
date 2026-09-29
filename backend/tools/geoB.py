from geopy.distance import geodesic
from geopy.point import Point


def get_bounding_box(latitude, longitude, distance):
    center = Point(latitude, longitude)
    # 5 km converted to meters for calculation
    radius = distance * 1000
    
    # Finding the north, south, east, and west points
    north = geodesic(kilometers=distance).destination(center, 0).latitude
    south = geodesic(kilometers=distance).destination(center, 180).latitude
    east = geodesic(kilometers=distance).destination(center, 90).longitude
    west = geodesic(kilometers=distance).destination(center, 270).longitude
    
    return {
        'north': north,
        'south': south,
        'east': east,
        'west': west
    }


# 範例經緯度
latitude = 22.774424
longitude = 120.399112

# 以給定經緯度為中心計算五公里範圍內的邊界經緯度
bounding_box = get_bounding_box(latitude, longitude, 5)

print("North:", bounding_box['north'])
print("South:", bounding_box['south'])
print("East:", bounding_box['east'])
print("West:", bounding_box['west'])
