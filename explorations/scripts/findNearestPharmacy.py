from qgis.core import *

# User location
# user_lat = 12.9716
# user_lon = 77.5946


# User location (example: Bangalore)
user_lat = 12.9784
user_lon = 77.6408

user_point = QgsPointXY(user_lon, user_lat)
user_geom = QgsGeometry.fromPointXY(user_point)

# Load pharmacy layer
pharmacy_layer = QgsProject.instance().mapLayersByName("amenity_pharmacy")[0]

nearest_feature = None
min_distance = float("inf")

for feature in pharmacy_layer.getFeatures():
    geom = feature.geometry()

    # Convert polygon to centroid point
    centroid = geom.centroid()

    distance = user_geom.distance(centroid)

    if distance < min_distance:
        min_distance = distance
        nearest_feature = feature

print("Nearest Pharmacy:", nearest_feature["name"])
print("Distance:", min_distance)