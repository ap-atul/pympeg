from pympeg._node import *
from pympeg._graph import *
from pympeg._util import *


class ffmpeg:
	def __init__(self):
		self._source = None
		self._sink = None

		# only for managing the index of the inputs
		self._input_nodes = list()

		self._filter_graph = Graph()

	def get_source_label(self, node):
		return '[%s]' % self._input_nodes.index(node)

	def input(self, name=None):
		node = IONode(name=name)
		self._input_nodes.append(node)

		if self._source is None:
			self._source = node

		node.set_out_label(self.get_source_label(node))
		self._filter_graph.add_node(node)

		return node

	def filter(self, *args, **kwargs):
		# start nodes
		inputs = args[0]

		# end node
		node = FilterNode(**kwargs)

		if isinstance(inputs, list or set or tuple):
			for inp in inputs:
				if isinstance(inp, IONode):
					node.add_input(inp.out_label)
				else:
					for outs in inp.outputs:
						node.add_input(outs)
				self._filter_graph.add_edge(inp, node)
		else:
			if isinstance(inputs, IONode):
				node.add_input(inputs.out_label)
				self._filter_graph.add_edge(inputs, node)

		return node

	def output(self, input_node, name=None):
		if name is not None:
			self._sink = IONode(name=name)

		for node in input_node.outputs:
			self._sink.add_input(node)

		return self._sink

	def graph(self, source):
		return self._filter_graph.traverse(source)

	def run(self):
		path = self._filter_graph.traverse(self._source)
		filter_nodes = list()
		result = list()

		for node in path:
			print(str(node))

		result.append("ffmpeg -y ")

		for node in path:
			if isinstance(node, IONode):
				result.append(get_str_from_ionode(node))
			else:
				filter_nodes.append(node)

		result.append(' -filter_complex "')
		for fil in filter_nodes:
			result.append(get_str_from_filter(fil))
		
		last_filter = result.pop()
		result.append(last_filter.replace(";", ""))

		result.append('"')

		for inp in self._sink.inputs:
			result.append(' -map "%s" '  % inp)

		result.append(" %s " % self._sink.params)

		return ''.join(result)


ffmpeg = ffmpeg()
input1 = ffmpeg.input("./example_01.mp4")
print(f"Input node :: {input1}")
filter1 = ffmpeg.filter(input1, filter_name="trim", params={"start": 2, "duration": 5})
filter1_1 = ffmpeg.filter(input1, filter_name="trim", params={"start": 2, "duration": 5})
filter2 = ffmpeg.filter([filter1, filter1_1], filter_name="concat", params={"n": 2, "a":1, "v":1}, outputs=2)
output = ffmpeg.output(filter2, "./output.mp4")
print(ffmpeg.run())
