from ._builder import Stream
from ._exceptions import *
from ._node import InputNode, FilterNode, Label, OutputNode, GlobalNode, stream
from ._util import get_str_from_filter, get_str_from_global

__all__ = ["input", "filter", "output", "arg", "run"]
s = Stream()


def _check_arg_type(args):
	flag = False

	for arg_ in args:
		if (
				isinstance(arg_, InputNode) or
				isinstance(arg_, FilterNode) or
				isinstance(arg_, GlobalNode) or
				isinstance(arg_, Label) or
				isinstance(arg_, list)
		):
			flag = True
			break

	return flag


def _get_label_param(value):
	if isinstance(value, Label):
		return value

	if isinstance(value, str):
		return Label(value)

	if isinstance(value, FilterNode):
		return value[0]

	if isinstance(value, InputNode):
		return Label(value.outputs)

	if isinstance(value, GlobalNode):
		return value[0]

	else:
		raise TypeMissing("Filter requires an filter or input type argument")


def _get_nodes_from_graph(graph):
	input_nodes, filter_nodes, global_nodes, output_nodes = list(), list(), list(), list()

	for node in graph:
		if isinstance(node, InputNode):
			input_nodes.append(node)

		if isinstance(node, FilterNode):
			filter_nodes.append(node)

		if isinstance(node, OutputNode):
			output_nodes.append(node)

		if isinstance(node, GlobalNode):
			global_nodes.append(node)

	node_len = len(input_nodes) + len(filter_nodes) + len(global_nodes) + len(output_nodes)
	assert node_len == len(graph)

	return input_nodes, filter_nodes, global_nodes, output_nodes


def _no_filter_command(input_nodes, output_node, cmd="ffmpeg"):
	"""
	Cases when there is no filter. Mostly when conversion is required.

	Example
	-------
	ex: convert .mp4 to .wav
		ffmpeg -y -i example.mp4 example.wav
	"""
	result = list()

	result.append(cmd)
	result.append(" -y")
	for inp in input_nodes:
		result.append(" -i %s " % inp.name)

	result.append(" %s" % output_node.pop().name)
	return ''.join(result)


def _get_command_from_graph(graph, cmd="ffmpeg"):
	result = list()
	input_nodes, filter_nodes, global_nodes, output_node = _get_nodes_from_graph(graph)

	# means that there is no filter
	if len(filter_nodes) == 0:
		return _no_filter_command(input_nodes, output_node)

	last_filter_node = filter_nodes.pop()

	result.append(cmd)
	for inp in input_nodes:
		result.append(" -i %s " % inp.name)

	result.append(' -y -filter_complex "')
	for filter_ in filter_nodes:
		result.append(get_str_from_filter(filter_))

	# adding global nodes
	for global_ in global_nodes:
		result.append(get_str_from_global(global_))

	# last filter should not have a semicolon at the end
	result.append(get_str_from_filter(last_filter_node).replace(";", ""))
	result.append('"')

	for out in output_node[0].inputs:
		result.append(' -map "[%s]"' % out.label)

	# output will be single
	result.append(" %s" % output_node[0].name)

	return ''.join(result)


@stream()
def input(name):
	if name is None:
		raise InputParamsMissing("File name required in input function")

	# creating a file input filter
	node = InputNode(name, s.count)

	# adding to the stream
	s.add(node).count += 1

	return node


@stream()
def filter(*args, **kwargs):
	if not _check_arg_type(args):
		raise TypeMissing("Filter requires an filter or input type argument")

	if len(kwargs) == 0:
		raise FilterParamsMissing

	# if explicit inputs are given skip caller
	if "inputs" in kwargs:
		inputs = kwargs["inputs"]
	# accept caller
	else:
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

	if isinstance(inputs, list):
		for inp in inputs:
			node.add_input(_get_label_param(inp))
	else:
		node.add_input(_get_label_param(inputs))

	s.add(node)
	return node


@stream()
def arg(caller=None, args=None, outputs=None, inputs=None):
	node = GlobalNode(args=args)

	# if inputs is there don't check caller
	if inputs is not None:
		if isinstance(inputs, list):
			for inp in inputs:
				node.add_input(_get_label_param(inp))
		else:
			node.add_input(_get_label_param(inputs))

	# if inputs is absent
	else:
		if isinstance(caller, list):
			for inp in caller:
				node.add_input(_get_label_param(inp))
		else:
			node.add_input(_get_label_param(caller))

	# adding outputs, if none then 1 output is created by default
	if isinstance(outputs, list):
		for out in outputs:
			node.add_output(_get_label_param(out))
	else:
		node.add_output(_get_label_param(outputs))

	s.add(node)
	return node


@stream()
def run(caller):
	if not isinstance(caller, OutputNode):
		raise OutputNodeMissingInRun

	graph = s.graph()
	command = _get_command_from_graph(graph)
	print(command)


@stream()
def graph(caller):
	return s.graph()
