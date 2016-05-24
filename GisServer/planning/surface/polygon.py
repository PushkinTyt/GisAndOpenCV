class PolygonProjection:
	def __init__(self, vertices, polygon, area_factor, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		self.__vertices    = tuple(vertices)
		self.__polygon     = polygon
		self.__area_factor = area_factor
		
		
		
		
		
	@property
	def vertices(self):
		return self.__vertices
		
		
		
	@property
	def polygon(self):
		return self.__polygon
		
		
		
	@property
	def area_factor(self):
		return self.__area_factor
		
		
		
		
		
	@property
	def area(self):
		area = self.__area_factor * self.projection_area
		
		return area
		
		
		
	@property
	def projection_area(self):
		first_length  = abs(self.__vertices[1] - self.__vertices[0])
		second_length = abs(self.__vertices[2] - self.__vertices[1])
		third_length  = abs(self.__vertices[0] - self.__vertices[2])
		
		half_perimeter = (first_length + second_length + third_length) / 2
		
		projection_area_square = \
			half_perimeter \
				* (half_perimeter - first_length) \
				* (half_perimeter - second_length) \
				* (half_perimeter - third_length)
				
		#!!!!! Подумать как сделать лучше. Вероятно из-за ошибки вычислений
		#!!!!! может оказаться, что квадрат площади отрицателен (когда одна
		#!!!!! из сторон мала)
		if projection_area_square <= 0:
			projection_area = 0
		else:
			projection_area = projection_area_square ** 0.5
			
		return projection_area
		
		
		
		
		
		
		
class Polygon:
	def __init__(self, vertices, penalty, impassability, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		
		self.__vertices      = tuple(vertices)
		self.__penalty       = penalty
		self.__impassability = impassability
		
		
		
		first_vector = \
			[first_coordinate - second_coordinate \
				for first_coordinate, second_coordinate \
				in zip(self.__vertices[1], self.__vertices[0])]
				
		second_vector = \
			[first_coordinate - second_coordinate \
				for first_coordinate, second_coordinate \
				in zip(self.__vertices[2], self.__vertices[1])]
				
		third_vector = \
			[first_coordinate - second_coordinate \
				for first_coordinate, second_coordinate \
				in zip(self.__vertices[0], self.__vertices[2])]
				
				
				
		self.__normal = [
			first_vector[1] * second_vector[2] \
				- first_vector[2] * second_vector[1],
			first_vector[2] * second_vector[0] \
				- first_vector[0] * second_vector[2],
			first_vector[0] * second_vector[1] \
				- first_vector[1] * second_vector[0]
		]
		
		if self.__normal[2] < 0:
			self.__normal = [- coordinate for coordinate in self.__normal]
		elif self.__normal[2] == 0:
			raise Exception() #!!!!!
			
		normal_length = \
			sum([coordinate ** 2.0 for coordinate in self.__normal]) ** 0.5
			
		self.__normal = \
			[coordinate / normal_length for coordinate \
				in self.__normal]
				
		self.__normal = tuple(self.__normal)
		
		
		
		first_length = \
			sum([coordinate ** 2.0 for coordinate in first_vector]) ** 0.5
			
		second_length = \
			sum([coordinate ** 2.0 for coordinate in second_vector]) ** 0.5
			
		third_length = \
			sum([coordinate ** 2.0 for coordinate in third_vector]) ** 0.5
			
		half_perimeter = (first_length + second_length + third_length) / 2
		
		self.__area = \
			(half_perimeter \
				* (half_perimeter - first_length) \
				* (half_perimeter - second_length) \
				* (half_perimeter - third_length)) ** 0.5
				
				
				
				
				
	@property
	def vertices(self):
		return self.__vertices
		
		
		
	@property
	def penalty(self):
		return self.__penalty
		
		
		
	@property
	def impassability(self):
		return self.__impassability
		
		
		
	@property
	def normal(self):
		return self.__normal
		
		
		
	@property
	def area(self):
		return self.__area
		
		
		
		
		
	def get_projection(self):
		vertices = \
			[vertex[0] + vertex[1] * 1.0j for vertex \
				in self.__vertices]
				
				
		first_length  = abs(vertices[1] - vertices[0])
		second_length = abs(vertices[2] - vertices[1])
		third_length  = abs(vertices[0] - vertices[2])
		
		half_perimeter = (first_length + second_length + third_length) / 2
		
		area = \
			(half_perimeter \
				* (half_perimeter - first_length) \
				* (half_perimeter - second_length) \
				* (half_perimeter - third_length)) ** 0.5
				
				
		polygon_projection = \
			PolygonProjection(
				vertices,
				self,
				self.area / area
			)
			
		return polygon_projection
		