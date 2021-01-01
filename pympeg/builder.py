from pympeg.node import *
from pympeg.graph import *
from pympeg.utils import *


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
		output_node = self._filter_graph.pop()
		input_nodes = list()
		filter_nodes = list()
		result = list()

		for node in self._filter_graph:
			if isinstance(node, IONode):
				input_nodes.append(node)
			else:
				filter_nodes.append(node)

		result.append("ffmpeg -y ")
		for node in input_nodes:
			result.append(get_str_from_input(node))

		result.append(' -filter_complex "')
		last_filter = filter_nodes.pop()
		for node in filter_nodes:
			result.append(get_str_from_filter(node))
		result.append(get_str_from_filter(last_filter).replace(";", ""))

		result.append('" ')

		for out in last_filter.outputs:
			result.append(' -map "%s"' % out)
	
		result.append(get_str_from_output(output_node))

		return ''.join(result)



builder = Builder()
input_file = builder.input("example_01.mp4")
filter_trim = builder.filter(inputs="0", outputs="vtrim", filter_name="trim", params={"start":3, "duration": 10})
filter_trim = builder.filter(inputs="vtrim", outputs="v2trim", filter_name="trim", params={"start":3, "duration": 20})
output_file = builder.output("output.mp4")
result = builder.graph(input_file)
print(result)

