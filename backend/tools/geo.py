from geopy.distance import geodesic
from geopy.point import Point


def get_bounding_box(latitude, longitude, distance):
    center = Point(latitude, longitude)

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
