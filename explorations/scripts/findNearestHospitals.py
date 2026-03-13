from qgis.core import *

# User location
user_lat = 12.9716
user_lon = 77.5946

user_point = QgsPointXY(user_lon, user_lat)

hospital_layer = QgsProject.instance().mapLayersByName("healthcare_hospital")[0]

# Distance calculator
distance_calc = QgsDistanceArea()
distance_calc.setEllipsoid('WGS84')

nearest_feature = None
min_distance = float("inf")

for feature in hospital_layer.getFeatures():

    geom = feature.geometry()

    if geom is None or geom.isEmpty():
        continue

    # Convert polygons to centroid
    if geom.type() == QgsWkbTypes.PointGeometry:
        target_point = geom.asPoint()
    else:
        target_point = geom.centroid().asPoint()

    # Calculate geodesic distance in meters
    distance = distance_calc.measureLine(user_point, target_point)

    if distance < min_distance:
        min_distance = distance
        nearest_feature = feature

print("Nearest Hospital:", nearest_feature["name"])
print("Distance (km):", round(min_distance/1000, 2))