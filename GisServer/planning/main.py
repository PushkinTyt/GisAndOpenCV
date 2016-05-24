from planning.global_planning.graph \
	import GraphParameters, \
			GraphUtilities, \
			generate_graph
			
from planning.global_planning.planning \
	import estimate_graph
	
from planning.global_planning.visualization \
	import visualize_graph, \
			visualize_graph_estimation, \
			visualize_path
			
def MrkWayUpdate2(*a):
	pass
def DeleteWay(*a):
	pass
from planning.MrkWayUpdate \
	import MrkWayUpdate2, DeleteWay
	
from planning.surface.load_blender_surface \
	import load_blender_surface
	
from planning.surface.load_surface \
	import load_surface
	
from planning.surface.polygons_tree \
	import aaa
	
from planning.utilities.timer \
	import Timer
	
import math
import sys






latitude_scale            = 1 / 8.220e-6
longitude_scale           = 1 / 1.689e-5
is_visualization_required = False
map_file_name             = "planning/input"





try:
	with Timer("Загрузка поверхности:       %s с"):
		polygons_tree, min_lat, min_lon, max_lat, max_lon = \
			load_surface(map_file_name, latitude_scale, longitude_scale)
except:
	raise Exception("Поверхность не может быть обработана")
	
	
	
	
	
graph_parameters = GraphParameters()


graph_parameters.node_edge_size = 1.0
graph_parameters.origin         = 0.0

node_radius = \
	0.5 * graph_parameters.node_edge_size \
		/ math.sin(math.pi / 6.0)
graph_parameters.width = \
	(max_lon - min_lon) * longitude_scale \
		/ (node_radius + graph_parameters.node_edge_size / 2.0) \
		+ 1 #????? С запасом
graph_parameters.width = int(graph_parameters.width)
		
node_height = \
	0.5 * graph_parameters.node_edge_size \
		/ math.tan(math.pi / 6.0)
graph_parameters.height = \
	(max_lat - min_lat) * latitude_scale \
		/ (2.0 * node_height) \
		+ 1 #????? С запасом
graph_parameters.height = int(graph_parameters.height)
		
		
with Timer("Построение графа:           %s с"):
	graph = generate_graph(graph_parameters, polygons_tree)
	
if is_visualization_required:
	with open("graph.svg", "w") as output_file:
		with Timer("Прорисовка графа:           %s с"):
			visualize_graph(graph, graph_parameters, output_file)
			
			
			
			
			
def compute_path(start_point, end_point):
	"""
	[1] - КОНЕЧНАЯ ТОЧКА НЕ ЛЕЖИТ НА КАРТЕ
	[2] - путь до заданной точки не может быть проложен
	[3] - путь до заданнойточки не может быть проложен

	Возвращает:
	None - когда точки не лежат на карте
		(удалить путь)
	[] - когда путь между точками не может быть проложен (точки не связаны)
		(удалить путь)
	[_] - когда путь лежит на одном полигоне (нарисовать одну точку)
	[_ .. _] - все нормально, строим путь
	"""
	start_point = \
		(start_point[1] - min_lon) * longitude_scale \
			+ 1.0j * (start_point[0] - min_lat) * latitude_scale
			
	end_point = \
		(end_point[1] - min_lon) * longitude_scale \
			+ 1.0j * (end_point[0] - min_lat) * latitude_scale
			
			
			
	path_points = list()
	for c in [start_point, end_point]:
		path_points.append((c.real, c.imag))
	path_points = \
		[(latitude / latitude_scale + min_lat, \
				longitude / longitude_scale + min_lon) \
			for longitude, latitude in path_points]
	MrkWayUpdate2(path_points)


	graph_utilities = GraphUtilities(graph_parameters)
	start_node      = None
	end_node        = None
	
	with Timer("Определение кон. полигинов: %s с"):
		for node in graph_utilities.nodes(graph):
			if graph_utilities.contains_point(graph, node, start_point):
				start_node = node
				
				if end_node is not None:
					break
					
			if graph_utilities.contains_point(graph, node, end_point):
				end_node = node
				
				if start_node is not None:
					break
					
	if (start_node is None) and (end_node is None):
		DeleteWay()
		print("Маршрут не может быть проложен. Точки не лежат на карте")
		return "Маршрут не может быть проложен. Точки не лежат на карте"
	elif start_node is None:
		DeleteWay()
		print("Маршрут не может быть проложен. Начальная точка не лежит на карте")
		return "Маршрут не может быть проложен. Начальная точка не лежит на карте"
	elif end_node is None:
		DeleteWay()
		print("Маршрут не может быть проложен. Конечная точка не лежит на карте")
		return "Маршрут не может быть проложен. Конечная точка не лежит на карте"
		
		
		
		
		
	with Timer("Глобальное планирование:    %s с"):
		graph_estimation = estimate_graph(graph, graph_parameters, end_node)
		
	if is_visualization_required:
		with open("graph_estimation.svg", "w") as output_file:
			with Timer("Прорисовка оценок графа:    %s с"):
				visualize_graph_estimation(
					graph,
					graph_estimation,
					graph_parameters,
					output_file
				)
				
				
				
				
				
	q, r = start_node
	i, j = q, r // 2
	
	path = list()
	if graph_estimation[i][j] is not None:
		node = start_node
		
		while node is not None:
			path.append(node)
			
			q, r = node
			i, j = q, r // 2
			
			_, node = graph_estimation[i][j]
			
	path_points = list()
	# for node in graph_utilities.nodes(graph):
	for node in path:
		c = graph_utilities.compute_node_center(node)
		path_points.append((c.real, c.imag))
	# print((graph_parameters.width))
	# print((graph_parameters.height))
	# for i in range(graph_parameters.width):
	# 	for j in range(graph_parameters.height):
	# 		node = i, j * 2 + i % 2
	# 		c = graph_utilities.compute_node_center(node)
	# 		path_points.append((c.real, c.imag))
	path_points = \
		[(latitude / latitude_scale + min_lat, \
				longitude / longitude_scale + min_lon) \
			for longitude, latitude in path_points]
			
	if is_visualization_required:
		with open("path.svg", "w") as output_file:
			with Timer("Прорисовка пути:            %s с"):
				visualize_path(
					graph,
					path,
					graph_estimation,
					graph_parameters,
					output_file
				)
				
	if path_points:
		if len(path_points) == 1:
			path_points.append(
				path_points[0]
			)
		MrkWayUpdate2(path_points)
	else:
		DeleteWay()
		return "Маршрут не может быть проложен"
	return "Маршрут построен"
	
	
	
	
	
if __name__ == "__main__":
	start_point = float(sys.argv[1]), float(sys.argv[2])
	end_point   = float(sys.argv[3]), float(sys.argv[4])

	compute_path(start_point, end_point)
	