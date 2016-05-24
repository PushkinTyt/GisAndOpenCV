from planning.surface.polygons_tree import get_intersection

import cmath
import math





class GraphParameters:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.__width  = None
		self.__height = None
		self.__origin = None
		
		self.__node_edge_size = None
		
		
		
		
		
	@property
	def is_correct(self):
		is_correct = True
		
		is_correct &= self.__width is not None
		is_correct &= self.__height is not None
		is_correct &= self.__origin is not None
		is_correct &= self.__node_edge_size is not None
		
		return is_correct
		
		
		
	def copy(self):
		parameters = GraphParameters()
		
		parameters.__width     = self.__width
		parameters.__height    = self.__height
		parameters.__origin    = self.__origin
		parameters.__node_edge_size = self.__node_edge_size
		
		return parameters
		
		
		
		
		
	@property
	def width(self):
		return self.__width
		
		
	@width.setter
	def width(self, width):
		if width <= 0:
			raise Exception() #!!!!!
			
		self.__width = width
		
		
		
	@property
	def height(self):
		return self.__height
		
		
	@height.setter
	def height(self, height):
		if height <= 0:
			raise Exception() #!!!!!
			
		self.__height = height
		
		
		
	@property
	def origin(self):
		return self.__origin
		
		
	@origin.setter
	def origin(self, origin):
		self.__origin = origin
		
		
		
	@property
	def node_edge_size(self):
		return self.__node_edge_size
		
		
	@node_edge_size.setter
	def node_edge_size(self, node_edge_size):
		if node_edge_size <= 0.0:
			raise Exception() #!!!!!
			
		self.__node_edge_size = node_edge_size
		
		
		
		
		
		
		
class GraphUtilities:
	def __init__(self, graph_parameters, *args, **kwargs):
		if not graph_parameters.is_correct:
			raise Exception() #!!!!!
			
			
		super().__init__(*args, **kwargs)
		
		self.__graph_parameters = graph_parameters.copy()
		
		
		self.__node_area = \
			1.5 \
				* self.__graph_parameters.node_edge_size ** 2.0 \
				/ math.tan(math.pi / 6.0)
				
		self.__node_radius = \
			0.5 \
				* self.__graph_parameters.node_edge_size \
				/ math.sin(math.pi / 6.0)
				
		self.__node_height = \
			0.5 \
				* self.__graph_parameters.node_edge_size \
				/ math.tan(math.pi / 6.0)
				
				
				
				
				
	@property
	def graph_parameters(self):
		return self.__graph_parameters.copy()
		
		
		
		
		
	@property
	def node_area(self):
		return self.__node_area
		
		
		
	@property
	def node_radius(self):
		return self.__node_radius
		
		
		
	@property
	def node_height(self):
		return self.__node_height
		
		
		
	def compute_node_center(self, node):
		q, r = node
		
		node_center_imag_offset = r * self.__node_height
		node_center_real_offset = \
			q * self.__node_radius \
				+ q * 0.5 * self.__graph_parameters.node_edge_size
				
		node_center = \
			node_center_real_offset + 1.0j * node_center_imag_offset \
				+ self.__graph_parameters.origin
				
		return node_center
		
		
		
	def compute_node_vertices(self, node):
		node_center   = self.compute_node_center(node)
		node_vertices = \
			[cmath.rect(self.__node_radius, i * math.pi / 3.0) + node_center \
				for i \
				in range(6)]
				
		return node_vertices
		
		
		
		
		
	def contains_node(self, graph, node):
		"""
		graph должен соответствовать self.graph_parameters
		"""
		q, r = node
		i, j = q, r // 2
		
		
		contains_node = False
		
		if q % 2 == r % 2:
			if 0 <= i < self.__graph_parameters.width:
				if 0 <= j < self.__graph_parameters.height:
					if graph[i][j] is not None:
						contains_node = True
						
		return contains_node
		
		
		
	def nodes(self, graph):
		"""
		graph должен соответствовать self.graph_parameters
		"""
		for i in range(self.__graph_parameters.width):
			for j in range(self.__graph_parameters.height):
				node = i, 2 * j + i % 2
				
				if self.contains_node(graph, node):
					yield node
					
					
					
					
					
	def contains_point(self, graph, node, point):
		"""
		graph должен соответствовать self.graph_parameters
		"""
		if not self.contains_node(graph, node):
			raise Exception() #!!!!!
			
			
		node_center = self.compute_node_center(node)
		vertices    = self.compute_node_vertices(node)
		
		
		last_vertex = vertices[-1]
		
		for vertex in vertices:
			direction = vertex - last_vertex
			
			if direction.real != 0:
				line_coefficient = - (direction.imag / direction.real) + 1.0j
			else:
				line_coefficient = \
					1.0 - 1.0j * (direction.real / direction.imag)
					
			base_line_value = \
				(line_coefficient * vertex.conjugate() \
					+ line_coefficient.conjugate() * vertex).real
					
			line = \
				lambda point: \
					(line_coefficient * point.conjugate() \
						+ line_coefficient.conjugate() * point).real \
						- base_line_value
						
						
			node_center_value = line(node_center)
			point_value       = line(point)
			
			if node_center_value * point_value < 0.0:
				contains_point = False
				break
				
				
			last_vertex = vertex
		else:
			contains_point = True
			
			
		return contains_point
		
		
		
		
		
		
		
def generate_graph(graph_parameters, polygons_tree):
	graph_utilities = GraphUtilities(graph_parameters)
	
	
	def compute_node(node):
		node_vertices = graph_utilities.compute_node_vertices(node)
		intersection  = get_intersection(polygons_tree, node_vertices)
		
		
		if intersection:
			total_normal        = [0.0, 0.0, 0.0]
			total_penalty       = 0.0
			total_impassability = False
			
			total_area            = 0.0
			total_projection_area = 0.0
			
			for polygon_projection in intersection:
				normal        = polygon_projection.polygon.normal
				penalty       = polygon_projection.polygon.penalty
				impassability = polygon_projection.polygon.impassability
				
				
				total_normal[0] += normal[0] * polygon_projection.area
				total_normal[1] += normal[1] * polygon_projection.area
				total_normal[2] += normal[2] * polygon_projection.area
				
				total_penalty       += penalty * polygon_projection.area
				total_impassability |= impassability
				
				total_area            += polygon_projection.area
				total_projection_area += polygon_projection.projection_area
				
				
			projection_area_error = \
				abs(graph_utilities.node_area - total_projection_area)
				
			#!!!!! Вынести определение константы
			if projection_area_error < 0.0001:
				normal    = [0.0, 0.0, 0.0]
				normal[0] = total_normal[0] / total_area
				normal[1] = total_normal[1] / total_area
				normal[2] = total_normal[2] / total_area
				
				penalty       = total_penalty / total_area
				impassability = total_impassability
				
				if not impassability:
					result = normal, penalty, impassability
				else:
					result = None
			else:
				result = None
		else:
			result = None
			
			
		return result
		
		
	graph = \
		[[None] * graph_parameters.height for _ \
			in range(graph_parameters.width)]
			
	for i in range(graph_parameters.width):
		for j in range(graph_parameters.height):
			node = i, j * 2 + i % 2
			
			graph[i][j] = compute_node(node)
			
			
	return graph
	