from pympeg._node import *
from pympeg._graph import *


class ffmpeg():
	def __init__(self):
		self._source = None
		self._sink = None

		self._filter_graph = Graph()

	def get_source_label(self, node):
		return '[%s]' % (0)

	def input(self, name=None):
		if self._source is None:
			self._source = IONode(name=name)

		self._source.set_output_label(self.get_source_label(self._source))
		self._filter_graph.add_node(self._source)
		return self._source

	def filter(self, input_node, **kwargs):
		before = input_node
		node = FilterNode(**kwargs).set_input_label(before.out_label)
		
		self._filter_graph.add_edge((before, node))
		return node

	def output(self, input_node, name=None):
		if name is not None:
			self._sink = IONode(name=name)

		self._filter_graph.add_edge((input_node, self._sink))

		return self._sink

	def graph(self, source):
		return self._filter_graph.traverse(source)


ffmpeg = ffmpeg()
input1 = ffmpeg.input("input.mp4")
filter1 = ffmpeg.filter(input1, filter_name="trim", params={"st": 2, "d": 5})
filter2 = ffmpeg.filter(filter1, filter_name="clip", params={"q":3})
output = ffmpeg.output(filter2, "output.mp4")


path = ffmpeg.graph(input1)
for p in path:
	print(p)

