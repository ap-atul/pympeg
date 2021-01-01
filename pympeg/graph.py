""" Directed graph implementation """ 


class Graph:
	def __init__(self):
		self._graph = dict()

	def add_node(self, node):
		if node not in self._graph:
			self._graph[node] = list()
	
	def add_edge(self, before, after):
		if before in self._graph:
			self._graph[before].append(after)
			return

		self._graph[before] = [after]
	
	def traverse(self, source):
		graph = self._graph
		path = list()

		if source not in graph:
			return

		queue = [source] 

		# queue is non-empty
		while len(queue) != 0:
			start = queue.pop(0)

			if start not in path:
				path.append(start)

				# traversing the adjacent nodes
				for neighbour in graph[start]:
					path.append(neighbour)

		return path
