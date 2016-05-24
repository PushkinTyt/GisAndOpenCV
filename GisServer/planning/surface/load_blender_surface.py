from planning.surface.polygon       import Polygon
from planning.surface.polygons_tree import PolygonsTree







def load_blender_surface(surface_file, materials_file):
	materials_penalty       = dict()
	materials_impassability = dict()
	
	active_material = None
	
	for line in materials_file:
		line = line.split()
		
		if line:
			if line[0] == "newmtl":
				active_material = line[1]
			elif line[0] == "Kd":
				#!!!!! Задавать множитель в другом месте
				materials_penalty[active_material] = \
					255.0 * (1.0 - float(line[1]))
			elif line[0] == "Ks":
				materials_impassability[active_material] = \
					float(line[1]) == 0.0
					
					
	vertices = list()
	polygons = list()
	
	active_penalty       = None
	active_impassability = None
	
	for line in surface_file:
		line = line.split()
		
		if line:
			if line[0] == "v":
				vertex = [float(coordinate) for coordinate in line[1:]]
				
				vertices.append(vertex)
				
			elif line[0] == "usemtl":
				active_penalty       = materials_penalty[line[1]]
				active_impassability = materials_impassability[line[1]]
				
			elif line[0] == "f":
				polygon_vertices = \
					[vertices[int(vertex_index) - 1] \
						for vertex_index \
						in line[1:]]
						
				try:
					polygon = \
						Polygon(
							polygon_vertices,
							active_penalty,
							active_impassability
						)
						
					polygons.append(polygon)
				except:
					raise Exception() #!!!!!
					
					
	polygons_tree = PolygonsTree()
	
	for polygon in polygons:
		polygon_projection = polygon.get_projection()
		polygons_tree.add_polygon(polygon_projection)
		
	polygons_tree.break_polygons()
	
	
	return polygons_tree
	