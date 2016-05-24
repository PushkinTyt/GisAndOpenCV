from planning.surface.polygon import PolygonProjection







aaa = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
class PolygonsTree:
	def __init__(self, depth = 0, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		self.__depth = depth
		
		if self.__depth % 2 == 0:
			self.__coordinate = lambda c: c.real
		else:
			self.__coordinate = lambda c: c.imag
			
		self.__is_accumulation_stage = True
		self.__polygons              = set()
		self.__coordinates_sum       = 0.0
		
		self.__minimal_x = None
		self.__maximal_x = None
		self.__minimal_y = None
		self.__minimal_y = None
		
		
		
		
		
	@property
	def is_accumulation_stage(self):
		return self.__is_accumulation_stage
		
		
		
		
		
	def add_polygon(self, polygon):
		if not self.__is_accumulation_stage:
			raise Exception() #!!!!!
			
			
		for vertex in polygon.vertices:
			# if self.__minimal_x is None:
			# 	self.__minimal_x = vertex.real
			# 	self.__maximal_x = vertex.real
			# 	self.__minimal_y = vertex.imag
			# 	self.__maximal_y = vertex.imag
			# else:
			# 	self.__minimal_x = min(vertex.real, self.__minimal_x)
			# 	self.__maximal_x = max(vertex.real, self.__maximal_x)
			# 	self.__minimal_y = min(vertex.imag, self.__minimal_y)
			# 	self.__maximal_y = max(vertex.imag, self.__maximal_y)
				
			self.__coordinates_sum += self.__coordinate(vertex)
			
		self.__polygons.add(polygon)
		
		
		
	def add_polygons(self, polygons):
		if not self.__is_accumulation_stage:
			raise Exception() #!!!!!
			
			
		for polygon in polygons:
			self.add_polygon(polygon)
			
			
			
			
			
	def break_polygons(self):
		if not self.__is_accumulation_stage:
			raise Exception() #!!!!!
			
			
		median = \
			self.__coordinates_sum / (3 * len(self.__polygons))
			
		lesser_polygons  = list()
		greater_polygons = list()
		
		for polygon in self.__polygons:
			contains_lesser_vertices  = False
			contains_greater_vertices = False
			
			for vertex in polygon.vertices:
				if self.__coordinate(vertex) < median:
					contains_lesser_vertices = True
				elif self.__coordinate(vertex) > median:
					contains_greater_vertices = True
					
					
			if contains_lesser_vertices:
				lesser_polygons.append(polygon)
				
			if contains_greater_vertices:
				greater_polygons.append(polygon)
				
				
		are_polygons_breaked = \
			len(lesser_polygons) < len(self.__polygons) \
				and len(greater_polygons) < len(self.__polygons)
				
		if are_polygons_breaked:
			self.__is_leaf      = False
			self.__median       = median
			self.__lesser_tree  = PolygonsTree(self.__depth + 1)
			self.__greater_tree = PolygonsTree(self.__depth + 1)
			
			
			self.__lesser_tree.add_polygons(lesser_polygons)
			self.__lesser_tree.break_polygons()
			
			self.__greater_tree.add_polygons(greater_polygons)
			self.__greater_tree.break_polygons()
			
			del(self.__polygons)
		else:
			aaa[7] = max(aaa[7], self.__depth)
			self.__is_leaf = True
			
			
		self.__is_accumulation_stage = False
		
		
		
		
		
	def get_polygons(self, vertices):
		if self.__is_accumulation_stage:
			raise Exception() #!!!!!
			
			
		# left, right, bottom, top = True, True, True, True
		# for vertex in vertices:
		# 	if vertex.real >= self.__minimal_x:
		# 		left = False
		# 	if vertex.real <= self.__maximal_x:
		# 		right = False
		# 	if vertex.imag >= self.__minimal_y:
		# 		bottom = False
		# 	if vertex.imag <= self.__maximal_y:
		# 		top = False
				
		# if not any([left, right, bottom, top]):
		# 	aaa[4] += 1
		if not self.__is_leaf:
				# aaa[6] += 1
				# result_polygons  = self.__lesser_tree.get_polygons(vertices)
				# result_polygons |= self.__greater_tree.get_polygons(vertices)
			contains_lesser_vertices  = False
			contains_greater_vertices = False
			
			for vertex in vertices:
				if self.__coordinate(vertex) < self.__median:
					contains_lesser_vertices = True
				elif self.__coordinate(vertex) > self.__median:
					contains_greater_vertices = True
					
					
			result_polygons = set()
			
			if contains_lesser_vertices:
				result_polygons |= self.__lesser_tree.get_polygons(vertices)
				
			if contains_greater_vertices:
				result_polygons |= self.__greater_tree.get_polygons(vertices)
		else:
			result_polygons = set(self.__polygons)
		# else:
		# 	aaa[5] += 1
		# 	result_polygons = set()
			
			
		return result_polygons
		
		
		
		
		
		
		
def divide_polygon(vertices, polygon):
	center_point = sum(vertices) / len(vertices)
	
	
	def edges(vertices):
		last_vertex = vertices[-1]
		
		for vertex in vertices:
			yield last_vertex, vertex
			last_vertex = vertex
			
			
	def divide_polygon(first_vertex, second_vertex, polygon):
		vertices = polygon.vertices
		
		
		direction = second_vertex - first_vertex
		
		if direction.real != 0:
			line_coefficient = - (direction.imag / direction.real) + 1.0j
		else:
			line_coefficient = 1.0 - 1.0j * (direction.real / direction.imag)
			
		#!!!!! Разобраться со всеми именами
		lline = \
			lambda point: \
				line_coefficient * point.conjugate() \
					+ line_coefficient.conjugate() * point
					
					
		inner_vertices  = list()
		medium_vertices = list()
		outer_vertices  = list()
		
		base_line   = lline(first_vertex)
		center_line = lline(center_point) - base_line
		
		for vertex in vertices:
			line = lline(vertex) - base_line
			
			if (line * center_line).real > 0:
				inner_vertices.append((vertex, line))
			else:
				outer_vertices.append((vertex, line))
				
				
		if inner_vertices:
			for inner_vertex, inner_line in inner_vertices:
				for outer_vertex, outer_line in outer_vertices:
					k = - inner_line / (outer_line - inner_line)
					
					medium_vertices.append(
						k * (outer_vertex - inner_vertex) + inner_vertex
					)
					
			if len(medium_vertices) == 2:
				if len(inner_vertices) == 1:
					aaa[0] += 1
					sub_polygon = \
						PolygonProjection([
							inner_vertices[0][0],
							medium_vertices[0],
							medium_vertices[1]
						], polygon.polygon, polygon.area_factor)
						
					sub_polygons = [sub_polygon]
				else:
					aaa[1] += 1
					first_sub_polygon = \
						PolygonProjection([
							inner_vertices[0][0],
							medium_vertices[0],
							medium_vertices[1]
						], polygon.polygon, polygon.area_factor)
						
					second_sub_polygon = \
						PolygonProjection([
							inner_vertices[0][0],
							inner_vertices[1][0],
							medium_vertices[1]
						], polygon.polygon, polygon.area_factor)
						
					sub_polygons = [first_sub_polygon, second_sub_polygon]
			elif len(medium_vertices) == 1:
				aaa[2] += 1
				sub_polygons = [polygon]
				# sub_polygon = \
				# 	PolygonProjection([
				# 		inner_vertices[0][0],
				# 		inner_vertices[1][0],
				# 		medium_vertices[0]
				# 	], polygon.polygon, polygon.area_factor)
					
				# sub_polygons = [sub_polygon]
			else:
				aaa[3] += 1
				sub_polygons = [polygon]
				# sub_polygon = \
				# 	PolygonProjection([
				# 		inner_vertices[0][0],
				# 		inner_vertices[1][0],
				# 		inner_vertices[2][0]
				# 	], polygon.polygon, polygon.area_factor)
					
				# sub_polygons = [sub_polygon]
		else:
			sub_polygons = list()
			
			
		return sub_polygons
		
		
	sub_polygons = [polygon]
	last_vertex  = vertices[-1]
	
	for vertex in vertices:
		new_sub_polygons = list()
		
		for sub_polygon in sub_polygons:
			new_sub_polygons += \
				divide_polygon(last_vertex, vertex, sub_polygon)
				
		sub_polygons = new_sub_polygons
		last_vertex  = vertex
		
		
	return sub_polygons
	
	
	
	
	
def divide_polygons(polygons, vertices):
	sub_polygons = list()
	
	for polygon in polygons:
		sub_polygons += divide_polygon(vertices, polygon)
		
	return sub_polygons
	
	
	
	
	
def get_intersection(polygons_tree, vertices):
	polygons     = polygons_tree.get_polygons(vertices)
	intersection = divide_polygons(polygons, vertices)
	
	return intersection
	