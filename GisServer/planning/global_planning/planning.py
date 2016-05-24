from planning.utilities.priority_queue import PriorityQueue
from planning.global_planning.graph    import GraphUtilities







def estimate_graph(graph, graph_parameters, end_node):
	graph_utilities = GraphUtilities(graph_parameters)
	
	
	
	# Граф должен быть определен корректно
	if not graph_parameters.is_correct:
		raise Exception() #!!!!!
		
	# Целевая вершина должна принадлежать графу
	if not graph_utilities.contains_node(graph, end_node):
		raise Exception() #!!!!!
		
		
		
	# Массив оценок стоимостей достижения целевой позиции
	graph_estimation = \
		[[None] * graph_parameters.height for _ \
			in range(graph_parameters.width)]
			
			
			
	# Вычисление стоимостей и реализация очереди с приоритетом
	def get_record(node, predecessor_node = None):
		if predecessor_node is not None:
			node_center = \
				graph_utilities.compute_node_center(
					node
				)
				
			predecessor_node_center = \
				graph_utilities.compute_node_center(
					predecessor_node
				)
				
			edge_center = (node_center + predecessor_node_center) / 2.0
			
			
			node_offset             = edge_center - node_center
			predecessor_node_offset = edge_center - predecessor_node_center
			
			
			q, r = node
			i, j = q, r // 2
			
			node_normal, node_penalty, _ = graph[i][j]
			
			node_offset_x = node_offset.real
			node_offset_y = node_offset.imag
			node_offset_z = \
				- (node_normal[0] * node_offset_x \
					+ node_normal[1] * node_offset_y) / node_normal[2]
					
			node_transition_cost = \
				(node_offset_x ** 2.0 \
 					+ node_offset_y ** 2.0 \
 					+ node_offset_z ** 2.0) ** 0.5
					
			node_transition_cost *= node_penalty
			
			
			predecessor_q, predecessor_r = predecessor_node
			predecessor_i, predecessor_j = predecessor_q, predecessor_r // 2
			
			predecessor_node_normal, predecessor_node_penalty, _ = graph[i][j]
			
			predecessor_node_offset_x = predecessor_node_offset.real
			predecessor_node_offset_y = predecessor_node_offset.imag
			predecessor_node_offset_z = \
				- (predecessor_node_normal[0] * predecessor_node_offset_x \
					+ predecessor_node_normal[1] * predecessor_node_offset_y) \
				/ predecessor_node_normal[2]
				
			predecessor_node_transition_cost = \
				(predecessor_node_offset_x ** 2.0 \
 					+ predecessor_node_offset_y ** 2.0 \
 					+ predecessor_node_offset_z ** 2.0) ** 0.5
					
			predecessor_node_transition_cost *= predecessor_node_penalty
			
			
			transition_cost = \
				node_transition_cost \
					+ predecessor_node_transition_cost
					
			predecessor_cost, _ = \
				graph_estimation[predecessor_i][predecessor_j]
				
			cost = predecessor_cost + transition_cost
			
			
			record = cost, node, predecessor_node
		else:
			record = 0, node, predecessor_node
			
			
		return record
		
		
	def compare(first_record, second_record):
		first_cost, _, _  = first_record
		second_cost, _, _ = second_record
		
		return first_cost - second_cost
		
		
	priority_queue = PriorityQueue(compare)
	
	
	
	# Реализация алгоритма Дейкстры
	initial_record = get_record(end_node)
	priority_queue.push_value(initial_record)
	
	
	while not priority_queue.is_empty():
		# Извлечение из очереди самого дешевого перехода
		cost, node, predecessor_node = priority_queue.pop_least_value()
		
		# Вычисление индексов узла в графе и в задающем его массиве
		q, r = node
		i, j = q, r // 2
		
		
		# Если для узла еще нет стоимости, то извлечен самый дешевый переход
		# до него
		if graph_estimation[i][j] is None:
			# Заполнение массива оценок стоимостей
			graph_estimation[i][j] = (cost, predecessor_node)
			
			
			# Добавление смежных узлов графа в очередь
			possible_successor_nodes = [
				(q + 1, r + 1),
				(q + 1, r - 1),
				(q - 1, r + 1),
				(q - 1, r - 1),
				(q,     r + 2),
				(q,     r - 2)
			]
			
			for possible_successor_node in possible_successor_nodes:
				# Обрабатываются только узлы графа
				is_correct_node = \
					graph_utilities.contains_node(
						graph,
						possible_successor_node
					)
					
				if is_correct_node:
					successor_record = \
						get_record(
							possible_successor_node,
							node
						)
						
					priority_queue.push_value(successor_record)
					
					
					
	return graph_estimation
	