from planning.global_planning.graph import GraphUtilities

import svgwrite
import svgwrite.shapes







def visualize_graph(graph, graph_parameters, output_file = None):
	if not graph_parameters.is_correct:
		raise Exception() #!!!!!
		
		
	graph_utilities = GraphUtilities(graph_parameters)
	drawing         = svgwrite.Drawing()
	
	for node in graph_utilities.nodes(graph):
		node_view_points = \
			[(node_vertex.real * 1, - node_vertex.imag * 1) for node_vertex \
				in graph_utilities.compute_node_vertices(node)]
				
		node_view = \
			svgwrite.shapes.Polygon(
				node_view_points,
				fill           = svgwrite.rgb(0, 0, 0),
				fill_opacity   = 1.0,
				stroke         = svgwrite.rgb(0, 0, 0),
				stroke_width   = 0.1,
				stroke_opacity = 1.0
			)
			
		drawing.add(node_view)
		
		
	if output_file is not None:
		drawing.write(output_file)
	else:
		return drawing
		
		
		
		
		
def visualize_graph_estimation(graph,
								graph_estimation,
								graph_parameters,
								output_file = None):
	if not graph_parameters.is_correct:
		raise Exception() #!!!!!
		
		
		
	graph_utilities = GraphUtilities(graph_parameters)
	drawing         = svgwrite.Drawing()
	
	
	# Вычисление максимальной оценки по всем вершинам графа 
	max_cost = None
	
	for node in graph_utilities.nodes(graph):
		q, r = node
		i, j = q, r // 2
		
		if graph_estimation[i][j] is not None:
			cost, _ = graph_estimation[i][j]
			
			if max_cost is None:
				max_cost = cost
			else:
				max_cost = max(max_cost, cost)
				
				
	# Прорисовка узлов графа
	for node in graph_utilities.nodes(graph):
		q, r = node
		i, j = q, r // 2
		
		if graph_estimation[i][j] is not None:
			cost, _ = graph_estimation[i][j]
		else:
			cost, _ = None, None
			
			
		# Вычисление интенсивности узла в зависимости от оценки
		if cost is not None:
			if max_cost != 0:
				intensity = cost / max_cost
				intensity = round(255 - intensity * 200)
			else:
				intensity = 255
		else:
			intensity = 0
			
			
		# Добавление узла
		node_view_points = \
			[(node_vertex.real * 10000, - node_vertex.imag * 10000) for node_vertex \
				in graph_utilities.compute_node_vertices(node)]
				
		node_view = \
			svgwrite.shapes.Polygon(
				node_view_points,
				fill           = svgwrite.rgb(intensity, intensity, intensity),
				fill_opacity   = 1.0,
				stroke         = svgwrite.rgb(0, 0, 0),
				stroke_width   = 0.01,
				stroke_opacity = 1.0
			)
			
		drawing.add(node_view)
		
		
	# Прорисовка переходов
	for node in graph_utilities.nodes(graph):
		q, r = node
		i, j = q, r // 2
		
		if graph_estimation[i][j] is not None:
			_, predecessor_node = graph_estimation[i][j]
		else:
			predecessor_node = None
			
			
		if predecessor_node is not None:
			# Добавление перехода
			node_center = \
				graph_utilities.compute_node_center(node)
				
			predecessor_node_center = \
				graph_utilities.compute_node_center(predecessor_node)
				
				
			start = node_center.real * 10000, - node_center.imag * 10000
			end   = predecessor_node_center.real * 10000, - predecessor_node_center.imag * 10000
			
			transition_view = \
				svgwrite.shapes.Line(
					start          = start,
					end            = end,
					stroke         = svgwrite.rgb(0, 0, 0),
					stroke_width   = 0.1,
					stroke_opacity = 1.0
				)
				
			drawing.add(transition_view)
			
			
	if output_file is not None:
		drawing.write(output_file)
	else:
		return drawing
		
		
		
def visualize_path(graph, path, graph_estimation, graph_parameters,
					output_file = None):
	if not graph_parameters.is_correct:
		raise Exception() #!!!!!
		
		
		
	graph_utilities = GraphUtilities(graph_parameters)
	drawing         = svgwrite.Drawing()
	
	
	# Вычисление максимальной оценки по всем вершинам графа 
	max_cost = None
	
	for node in graph_utilities.nodes(graph):
		q, r = node
		i, j = q, r // 2
		
		if graph_estimation[i][j] is not None:
			cost, _ = graph_estimation[i][j]
			
			if max_cost is None:
				max_cost = cost
			else:
				max_cost = max(max_cost, cost)
				
				
	# Прорисовка узлов графа
	for node in graph_utilities.nodes(graph):
		q, r = node
		i, j = q, r // 2
		
		if graph_estimation[i][j] is not None:
			cost, _ = graph_estimation[i][j]
		else:
			cost, _ = None, None
			
			
		# Вычисление интенсивности узла в зависимости от оценки
		if cost is not None:
			if max_cost != 0:
				intensity = cost / max_cost
				intensity = round(255 - intensity * 200)
			else:
				intensity = 255
		else:
			intensity = 0
			
			
		# Добавление узла
		node_view_points = \
			[(node_vertex.real * 10000, - node_vertex.imag * 10000) for node_vertex \
				in graph_utilities.compute_node_vertices(node)]
				
		node_view = \
			svgwrite.shapes.Polygon(
				node_view_points,
				fill           = svgwrite.rgb(intensity, intensity, intensity),
				fill_opacity   = 1.0,
				stroke         = svgwrite.rgb(0, 0, 0),
				stroke_width   = 0.01,
				stroke_opacity = 1.0
			)
			
		drawing.add(node_view)
		
		
	# Прорисовка переходов
	for node in path:
		q, r = node
		i, j = q, r // 2
		
		if graph_estimation[i][j] is not None:
			_, predecessor_node = graph_estimation[i][j]
		else:
			predecessor_node = None
			
			
		if predecessor_node is not None:
			# Добавление перехода
			node_center = \
				graph_utilities.compute_node_center(node)
				
			predecessor_node_center = \
				graph_utilities.compute_node_center(predecessor_node)
				
				
			start = node_center.real * 10000, - node_center.imag * 10000
			end   = predecessor_node_center.real * 10000, - predecessor_node_center.imag * 10000
			
			transition_view = \
				svgwrite.shapes.Line(
					start          = start,
					end            = end,
					stroke         = svgwrite.rgb(0, 0, 0),
					stroke_width   = 0.1,
					stroke_opacity = 1.0
				)
				
			drawing.add(transition_view)
			
			
	if output_file is not None:
		drawing.write(output_file)
	else:
		return drawing
		