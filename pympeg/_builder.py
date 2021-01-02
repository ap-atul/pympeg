class Stream:
	def __init__(self):
		self._stream = list()
		self.count = 0

	def add(self, node):
		self._stream.append(node)
		return self

	def graph(self):
		return self._stream
