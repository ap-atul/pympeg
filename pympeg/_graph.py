""" Simple directed graph implementation """


class Graph:
	""" Stores the connection between the filters """
	def __init__(self):
		self.graph = dict()

	def __str__(self):
		string = list()
		for key, values in self.graph.items():

			string.append(str(key))
			for f in values:
				string.append(str(f))

		return ''.join(string)

	def add_node(self, node):
		if node not in self.graph:
			self.graph[node] = list()

	def add_edge(self, before, after_node):
		if before in self.graph:
			self.graph[before].append(after_node)
		else:
			self.graph[before] = [after_node]

	def traverse(self, source):
		graph = self.graph

		if source is None or source not in graph:
			return None

		path = list()
		queue = [source]

		while len(queue) != 0:
			s = queue.pop(0)

			if s not in path:
				path.append(s)

				if s in graph:
					for neighbour in graph[s]:
						queue.append(neighbour)

		return path
