from ._builder import Stream
from ._exceptions import *
from ._node import InputNode, FilterNode, Label, OutputNode, stream

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


@stream()
def input(name):
	if name is None:
		raise FileNameMissing("File name required in input function")

	# creating a file input node
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
	for node in graph:
		print(str(node))


__all__ = ["input", "filter", "output", "run"]
