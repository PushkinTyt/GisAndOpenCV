import heapq







class PriorityQueueElement:
	def __init__(self, value, compare, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.__value   = value
		self.__compare = compare
		
		
		
		
		
	@property
	def value(self):
		return self.__value
		
		
		
	@property
	def compare(self):
		return self.__compare
		
		
		
		
		
	def __eq__(self, element):
		return self.__compare(self.__value, element.__value) == 0
		
		
		
	def __ne__(self, element):
		return self.__compare(self.__value, element.__value) != 0
		
		
		
	def __lt__(self, element):
		return self.__compare(self.__value, element.__value) < 0
		
		
		
	def __gt__(self, element):
		return self.__compare(self.__value, element.__value) > 0
		
		
		
	def __le__(self, element):
		return self.__compare(self.__value, element.__value) <= 0
		
		
		
	def __ge__(self, element):
		return self.__compare(self.__value, element.__value) >= 0
		
		
		
		
		
		
		
class PriorityQueue:
	def __init__(self, compare, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.__elements = list()
		self.__compare  = compare
		
		
		
		
		
	@property
	def compare(self):
		return self.__compare
		
		
		
		
		
	def is_empty(self):
		return len(self.__elements) == 0
		
		
		
	def push_value(self, value):
		element = PriorityQueueElement(value, self.__compare)
		
		heapq.heappush(self.__elements, element)
		
		
		
	def pop_least_value(self):
		least_element = heapq.heappop(self.__elements)
		least_value   = least_element.value
		
		return least_value
		