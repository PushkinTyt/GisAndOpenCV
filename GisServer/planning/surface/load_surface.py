from planning.surface.polygon       import Polygon
from planning.surface.polygons_tree import PolygonsTree







def load_surface(input_file_name, latitude_scale, longitude_scale):
	minimal_latitude  = None
	minimal_longitude = None
	maximal_latitude  = None
	maximal_longitude = None
	
	with open(input_file_name, "r") as input_file:
		for line in input_file:
			line = line.split()
			
			minimal_polygon_latitude = \
				min([
					float(line[0]),
					float(line[2]),
					float(line[4]),
				])
			minimal_polygon_longitude = \
				min([
					float(line[1]),
					float(line[3]),
					float(line[5]),
				])
			maximal_polygon_latitude = \
				max([
					float(line[0]),
					float(line[2]),
					float(line[4]),
				])
			maximal_polygon_longitude = \
				max([
					float(line[1]),
					float(line[3]),
					float(line[5]),
				])
				
			if minimal_latitude is None:
				minimal_latitude  = minimal_polygon_latitude
				minimal_longitude = minimal_polygon_longitude
				maximal_latitude  = maximal_polygon_latitude
				maximal_longitude = maximal_polygon_longitude
			else:
				minimal_latitude  = \
					min(minimal_polygon_latitude, minimal_latitude)
				minimal_longitude = \
					min(minimal_polygon_longitude, minimal_longitude)
				maximal_latitude  = \
					max(maximal_polygon_latitude, maximal_latitude)
				maximal_longitude = \
					max(maximal_polygon_longitude, maximal_longitude)
					
					
	polygons_projections = list()
	
	with open(input_file_name, "r") as input_file:
		for line in input_file:
			line = line.split()
			
			coordinates = [float(value) for value in line[:6]]
			
			x_coordinates = \
				[longitude_scale * (longitude - minimal_longitude) \
					for longitude \
					in (coordinates[1], coordinates[3], coordinates[5])]
			y_coordinates = \
				[latitude_scale * (latitude - minimal_latitude) \
					for latitude \
					in (coordinates[0], coordinates[2], coordinates[4])]
			z_coordinates = [0.0] * 3
			
			vertices      = zip(x_coordinates, y_coordinates, z_coordinates)
			penalty       = float(line[6])
			impassability = True if line[-1] == "True" else False
			
			polygon            = Polygon(vertices, penalty, impassability)
			polygon_projection = polygon.get_projection()
			polygons_projections.append(polygon_projection)
			
	polygons_tree = PolygonsTree()
	polygons_tree.add_polygons(polygons_projections)
	polygons_tree.break_polygons()
	
	return polygons_tree, minimal_latitude, minimal_longitude, \
			maximal_latitude, maximal_longitude
			