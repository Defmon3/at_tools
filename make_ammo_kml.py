#!/usr/bin/env python3

import math

# Your full list of coordinates (replace this with your actual complete list)
coordinates_list = [
    (54.1628, 45.1759),
    (57.9821, 33.0219),
    (53.2243, 34.3963),
    (61.8792, 33.9705),
    (56.3599, 38.4498),
    (59.9476, 29.5283),
    (53.2209, 36.4361),
    (56.6788, 61.1018),
    (54.8297, 20.4527),
    (55.7162, 43.8753),
    (57.8561, 53.2782),
    (60.7092, 29.9557),
    (55.8759, 39.6281),
    (44.6011, 33.6711),
    (55.8710, 39.1206),
    (44.9190, 41.1687),
    (53.8747, 48.4296),
    (56.1001, 38.7500),
    (56.2587, 34.1164),
    (56.2672, 34.3043),
    (55.8524, 37.7159),
    (54.5152, 36.3202),
    (53.1426, 34.9483),
    (45.8859, 40.0403),
    (54.9310, 37.4075),
    (54.2895, 37.5948),
    (50.4264, 136.8503),
    (44.0032, 131.9141),
    (56.7619, 35.7044),
    (49.2031, 140.2415),
    (51.4238, 46.2596),
    (54.2648, 34.4226),
    (58.1472, 30.3276),
    (48.3200, 41.7907),
    (54.3098, 32.3547),
    (44.6642, 33.5930),
    (59.0983, 38.6155),
    (50.5635, 35.7384),
    (50.5306, 35.7677),
    (56.2841, 93.5828),
    (48.1810, 135.0337),
    (56.2501, 38.3087),
    (53.5587, 33.9708),
    (51.3604, 41.9194),
    (53.4507, 102.5916),
    (55.4260, 35.7669),
    (58.6157, 59.6363),
    (54.7726, 58.6223),
    (54.8029, 58.6386),
    (51.1840, 46.0215),
    (50.2939, 137.4648),
    (51.5115, 113.0401),
    (54.7971, 20.3126),
    (54.8367, 20.3538),
    (60.4794, 29.2495),
    (54.7594, 20.1299),
    (50.0151, 136.4446),
    (50.1547, 129.4569),
    (58.4806, 33.5007),
    (56.3570, 31.6500),
    (55.8711, 39.1206),
    (56.1001, 38.7500),
    (56.2584, 43.2617),
    (56.2486, 34.1262),
    (56.2672, 34.3043),
    (55.8527, 37.7090),
    (54.5083, 36.3239),
    (53.1425, 34.9520),
    (43.7395, 44.5222),
    (56.9900, 60.7998),
    (56.1523, 41.4625),
    (54.9309, 37.4135),
    (55.0153, 73.3936),
    (58.2651, 43.8476),
    (53.9422, 46.7230),
    (57.9821, 33.0219),
    (56.5042, 31.7098),
    (53.2243, 34.3963),
    (55.4314, 41.5442),
    (54.5879, 20.2047),
    (54.9265, 38.4925),
    (54.0031, 101.8431),
    (47.4424, 40.0987),
    (52.5189, 39.7484),
    (54.7270, 20.1699),
    (59.9719, 29.3124),
    (58.4340, 41.5514),
    (57.9700, 38.3904),
    (56.3091, 42.9241),
    (60.4794, 29.2495),
    (54.7594, 20.1299),
    (50.0151, 136.4446),
    (50.1547, 129.4569),
    (58.4806, 33.5007),
    (56.3570, 31.6500),
    (55.8711, 39.1206),
    (56.1001, 38.7500),
    (56.2584, 43.2617),
    (56.2486, 34.1262),
    (56.2672, 34.3043),
    (55.8527, 37.7090),
    (54.5083, 36.3239),
    (53.1425, 34.9520),
    (43.7395, 44.5222),
    (56.9900, 60.7998),
    (56.1523, 41.4625),
    (54.9309, 37.4135),
    (55.0153, 73.3936),
    (58.2651, 43.8476),
    (53.9422, 46.7230),
    (57.9821, 33.0219),
    (56.5042, 31.7098),
    (53.2243, 34.3963),
    (55.4314, 41.5442),
    (54.5879, 20.2047),
    (54.9265, 38.4925),
    (54.0031, 101.8431),
    (47.4424, 40.0987),
    (52.5189, 39.7484),
    (54.7270, 20.1699),
    (59.9719, 29.3124),
    (58.4340, 41.5514),
    (57.9700, 38.3904),
    (56.3091, 42.9241),
    (69.0114, 33.6504),
    (68.2425, 33.8687),
    (42.8782, 132.3239),
    (69.3887, 32.4394),
    (52.9454, 158.3769),
    (69.2489, 33.3608),
    (54.8785, 20.0355),
    (55.9093, 49.2588),
    (57.6895, 33.9850),
    (69.0314, 33.1865),
    (69.0423, 33.1236),
    (56.7424, 60.4452),
    (68.5143, 33.2640),
    (57.5658, 34.6679),
    (54.8293, 20.4925),
    (54.8284, 20.5544),
    (55.2802, 62.7281),
    (60.9729, 29.1986),
    (60.9624, 29.0212),
    (54.5519, 36.3572),
    (69.3875, 32.4412),
    (69.0949, 33.5002),
    (69.2482, 33.3627),
    (59.5269, 30.3434),
    (52.7367, 41.6239),
    (60.4327, 28.7322),
    (69.0339, 33.6401),
    (57.7509, 28.2584),
    (64.5154, 40.1464),
    (67.9957, 34.4023),
    (52.7004, 41.6637),
    (61.9317, 34.2375),
    (54.8596, 73.3986),
    (69.0600, 33.3983),
    (56.2263, 90.5156),
    (69.0611, 33.3759),
    (52.4678, 44.2077),
    (56.4970, 53.6848),
    (54.9568, 73.3990),
    (54.9481, 73.4683),
    (58.0984, 38.7312),
    (68.8322, 33.1115),
    (69.0203, 33.6430),
    (55.8596, 36.8668),
    (60.0496, 30.4883),
    (69.1127, 33.5196),
    (64.4437, 40.7094),
    (55.6493, 61.6423),
    (51.6190, 39.0960),
    (58.2652, 43.8476),
    (57.4553, 40.2998),
    (48.9961, 44.2152),
    (46.5737, 40.5929),
    (48.0488, 39.6307),
    (48.0699, 39.6814),
    (48.0912, 39.7238),
    (48.1190, 39.6447),
    (48.0892, 39.5869),
    (48.2670, 39.9097),
    (48.6109, 39.2526),
    (48.6077, 39.2914),
    (48.5810, 39.2632),
    (48.0582, 39.6742),
    (48.1542, 39.5220),
    (48.0768, 39.3449),
    (48.1639, 39.5141)
]

# Number of points in the polygon
num_points = 24

# Calculate the angular spacing between points
angle_step = 2 * math.pi / num_points

# KML template (modified to include multiple Placemarks)
kml_template = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    {placemarks}
  </Document>
</kml>
"""


# Function to generate a polygon for a single coordinate pair
def generate_polygon(center_lat, center_lon, radius):
    polygon_coords = []
    for i in range(num_points):
        angle = i * angle_step
        x_offset = radius * math.cos(angle)
        y_offset = radius * math.sin(angle)
        point_lon = center_lon + x_offset / (111132 * math.cos(math.radians(center_lat)))
        point_lat = center_lat + y_offset / 111132
        polygon_coords.append(f"{point_lon},{point_lat}")

    # Create a KML Placemark for the polygon
    placemark = """<Placemark>
      <name>Polygon</name>
      <Polygon>
        <extrude>1</extrude>
        <altitudeMode>relativeToGround</altitudeMode>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>
              {coordinates}
            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>"""
    return placemark.format(coordinates="\n".join(polygon_coords))


# Generate polygons and KML
placemarks = []
for center_lat, center_lon in coordinates_list:
    placemarks.append(generate_polygon(center_lat, center_lon, 1000))

filled_kml = kml_template.format(placemarks="\n".join(placemarks))

# Save the KML to a file
filename = "polygons.kml"
with open(filename, "w") as kml_file:
    kml_file.write(filled_kml)

print(f"KML file saved as: {filename}")
