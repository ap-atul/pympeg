""" Simple directed graph implementation """

class Graph:
	def __init__(self):
		self.graph = dict()

	def __str__(self):
		for key, values in self.graph.items():
			string = list()

			string.append(str(key))
			for f in values:
				string.append(str(f))

		return ''.join(string)

	def add_node(self, node):
		if node not in self.graph:
			self.graph[node] = list()

	def add_edge(self, edge, label=None):
		node, after_node = edge

		if label is None:
			label = node.out_label
	
		after_node.set_input_label = label

		if node in self.graph:
			self.graph[node].append(after_node)
		else:
			self.graph[node] = [after_node]

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
				else:
					print("not is graph", s)

		return path
