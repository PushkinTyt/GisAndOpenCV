from PIL import Image

import itertools
import sys

penalty_dict = {(128, 255, 128, 255):100,
                (251, 253, 250, 255):1,
                (255, 0, 0, 255): 50,
                (255, 254, 122, 255):10}
impassability_dict = {(128, 255, 128, 255):True,
                (251, 253, 250, 255):False,
                (255, 0, 0, 255): False,
                (255, 254, 122, 255):False}

map_flie_name = sys.argv[1]
min_lat = float(sys.argv[2])
min_lon = float(sys.argv[3])
max_lat = float(sys.argv[4])
max_lon = float(sys.argv[5])
lat_step_size = float(sys.argv[6])
lon_step_size = float(sys.argv[7])
output_file_name = sys.argv[8]

lat_steps_number = int((max_lat - min_lat) / lat_step_size)
lon_steps_number = int((max_lon - min_lon) / lon_step_size)
poygons_indicies = \
	itertools.product(
		range(lat_steps_number),
		range(lon_steps_number)
	)

polygons = list()
for i, j in poygons_indicies:
	x = i * lat_step_size + min_lat
	y = j * lon_step_size + min_lon

	first_polygon = [
		(x, y),
		(x + lat_step_size, y),
		(x + lat_step_size, y + lon_step_size),
	]
	second_polygon = [
		(x, y),
		(x + lat_step_size, y + lon_step_size),
		(x, y + lon_step_size),
	]

	polygons.append(first_polygon)
	polygons.append(second_polygon)

image = Image.open(map_flie_name)
def convert_coordinates(x, y):
	i = int((x - min_lat) / (max_lat - min_lat))
	j = int((y - min_lon) / (max_lon - min_lon))
	return i, j

def get_penalty(polygon):
	total_x = 0.0
	total_y = 0.0
	for x, y in polygon:
		total_x += x
		total_y += y
	mean_x = int(total_x / 3.0)
	mean_y = int(total_y / 3.0)

	color = \
		image.getpixel(
			convert_coordinates(mean_x, mean_y)
        )

    penalty = penalty_dict[color]
    impassability = impassability_dict[color]

	return penalty, impassability

with open(output_file_name, "w") as output_file:
	for polygon in polygons:
		line = ""
		for x, y in polygon:
			line += "%s " % x
			line += "%s " % y
		line += "%s" % get_penalty(polygon)
		output_file.write(line + "\n")
