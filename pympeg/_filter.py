from ._builder import Stream
from ._exceptions import *
from ._node import InputNode, FilterNode, Label, OutputNode, stream
from ._util import get_str_from_filter

__all__ = ["input", "filter", "output", "run"]
s = Stream()


def _check_arg_type(args):
	flag = False

	for arg in args:
		if (
				isinstance(arg, InputNode) or
				isinstance(arg, FilterNode) or
				isinstance(arg, Label)
		):
			flag = True
			break

	return flag


def _get_label_param(inputs):
	if isinstance(inputs, Label):
		return inputs

	if isinstance(inputs, FilterNode):
		return inputs[0]

	if isinstance(inputs, InputNode):
		return Label(str(s.count - 1))

	else:
		raise TypeMissing("Filter requires an filter or input type argument")


def _get_nodes_from_graph(graph):
	input_nodes, filter_nodes, output_nodes = list(), list(), list()

	for node in graph:
		if isinstance(node, InputNode):
			input_nodes.append(node)

		if isinstance(node, FilterNode):
			filter_nodes.append(node)

		if isinstance(node, OutputNode):
			output_nodes.append(node)

	node_len = len(input_nodes) + len(filter_nodes) + len(output_nodes)
	assert node_len == len(graph)

	return input_nodes, filter_nodes, output_nodes


def _get_command_from_graph(graph, cmd="ffmpeg"):
	result = list()
	input_nodes, filter_nodes, output_node = _get_nodes_from_graph(graph)
	last_filter_node = filter_nodes.pop()

	result.append(cmd)
	for inp in input_nodes:
		result.append(" -i %s " % inp.name)

	result.append(' -y -filter_complex "')
	for filter_ in filter_nodes:
		result.append(get_str_from_filter(filter_))

	# last filter should not have a semicolon at the end
	result.append(get_str_from_filter(last_filter_node).replace(";", ""))
	result.append('"')

	for out in last_filter_node.outputs:
		result.append(' -map "[%s]"' % out.label)

	# output will be single
	result.append(" %s" % output_node[0].name)

	return ''.join(result)


@stream()
def input(name):
	if name is None:
		raise FileNameMissing("File name required in input function")

	# creating a file input filter
	node = InputNode(name)

	# adding to the stream
	s.add(node).count += 1

	return node


@stream()
def filter(*args, **kwargs):
	if not _check_arg_type(args):
		raise TypeMissing("Filter requires an filter or input type argument")

	if len(kwargs) == 0:
		raise FilterParamsMissing

	inputs = args[0]
	filter_node = FilterNode(**kwargs)

	if isinstance(inputs, list):
		for inp in inputs:
			filter_node.add_input(_get_label_param(inp))
	else:
		filter_node.add_input(_get_label_param(inputs))

	s.add(filter_node)
	return filter_node


@stream()
def output(*args, **kwargs):
	if not _check_arg_type(args):
		raise TypeMissing("Output requires an filter or input type argument")

	if "name" not in kwargs:
		return None

	node = OutputNode(name=kwargs["name"])
	inputs = args[0]

	if not isinstance(inputs, FilterNode):
		raise TypeMissing("Output requires an filter or input type argument")

	if isinstance(inputs, list):
		for inp in inputs:
			node.add_input(_get_label_param(inp))
	else:
		node.add_input(_get_label_param(inputs))

	s.add(node)
	return node


@stream()
def run(caller):
	if not isinstance(caller, OutputNode):
		raise Exception

	graph = s.graph()
	command = _get_command_from_graph(graph)
	print(command)
