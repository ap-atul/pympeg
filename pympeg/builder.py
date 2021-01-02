from pympeg.node import *
from pympeg.graph import *
from pympeg.utils import *


class Builder:
	def __init__(self):
		self._filter_graph = list()

	def input(self, node):
		self._filter_graph.append(node)

		return self

	def filter(self, node):
		self._filter_graph.append(node)

		return self

	def output(self, node):
		self._filter_graph.append(node)

		return self

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


b = Builder()
trim_labels = gen_labels(n=10)
print(trim_labels)
input1 = IONode(name="example_01.mp4")
intro = IONode(name="gretel_small.mkv")
extro = IONode(name="gretel_small.mkv")

trim_filter_a = FilterNode("0:v", "vtrim", "trim", {"start": 2, "duration": 10})
trim_filter_b = FilterNode("0:v", ["video"], "trim", {"start": 5, "duration": 7})
scale_filter_a = FilterNode("vtrim", "vscale", "scale", {"h":1280, "w": -1})
crop_filter_a = FilterNode("vscale", "cscale", "crop", {"h":1280, "w": 720})
scale_filter_b = FilterNode("video", "vscale2", "scale", {"h":1280, "w": -1})
crop_filter_b = FilterNode("vscale2", "cscale2", "crop", {"h":1280, "w": 720})
concat_filter = FilterNode(["1:v", "1:a", "cscale", "0:a", "cscale2", "0:a", "2:v", "2:a"], ["vid", "aud"], "concat", {"n": 4, "v": 1, "a": 1})
output = IONode(name="output.mp4")

string = b.input(input1).input(intro).input(extro).filter(trim_filter_a).filter(scale_filter_a).filter(crop_filter_a).filter(trim_filter_b).filter(scale_filter_b).filter(crop_filter_b).filter(concat_filter).output(output).graph(input1)
print(string)




