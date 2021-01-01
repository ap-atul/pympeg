from pympeg.node import *
from pympeg.graph import *


class Builder:
	def __init__(self):
		self._filter_graph = list()

	def input(self, name=None):
		node = IONode(name=name)
		self._filter_graph.append(node)
		
		return node

	def filter(self, **kwargs):
		node = FilterNode(**kwargs)
		self._filter_graph.append(node)
		return node

	def output(self, name=None):
		node = IONode(name=name)
		self._filter_graph.append(node)
		return node

	def graph(self, source):

		for p in self._filter_graph:
			print(str(p))


builder = Builder()
input_file = builder.input("input.mp4")
filter_trim = builder.filter(inputs="0", outputs="vtrim", filter_name="trim", params={"start":3})
filter_trim = builder.filter(inputs="vtrim", outputs="v2trim", filter_name="trim", params={"start":3})
output_file = builder.output("output.mp4")
builder.graph(input_file)

