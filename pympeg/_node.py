from ._exceptions import *
from ._util import gen_labels


class Label:
	def __init__(self, label=None):
		if label is None:
			self._label = gen_labels()
		else:
			self._label = label

	def __repr__(self):
		return "[%s]" % self._label

	def __eq__(self, other):
		return self.label == other.label

	@property
	def label(self):
		return self._label

	def set_label(self, label):
		self._label = label
		return self


class InputNode:
	def __init__(self, name, output):
		if name is None or output is None:
			raise InputParamsMissing

		self._name = name
		self._output = str(output)

	def __repr__(self):
		return "@input %s" % self._name + " :output [%s]" % self._output

	@property
	def name(self):
		return self._name

	@property
	def audio(self):
		return self._output + ":a"

	@property
	def video(self):
		return self._output + ":v"

	@property
	def outputs(self):
		return "%s" % self._output

	def set_name(self, name):
		self._name = name
		return self


class OutputNode:
	def __init__(self, name=None, inputs=None):
		self._name = name
		self._inputs = list()

		if inputs is not None:
			self._inputs = inputs

	def __repr__(self):
		result = list()
		result.append("@output %s :input=" % self._name)

		for inp in self._inputs:
			result.append("%s " % inp)

		return ''.join(result)

	@property
	def name(self):
		return self._name

	@property
	def inputs(self):
		return self._inputs

	def set_name(self, name):
		self._name = name
		return self

	def add_input(self, label):
		self._inputs.append(label)
		return self


class FilterNode:
	def __init__(self, filter_name=None, params=None, inputs=None, outputs=1):
		self._filter = filter_name
		self._params = dict()
		self._inputs = list()
		self._outputs = list()

		for _ in range(outputs):
			self._outputs.append(Label())

		if inputs is not None:
			self._inputs = inputs

		if params is not None:
			self._params = params

	def __repr__(self):
		result = list()
		result.append("@filter %s :input=" % self._filter)

		for inp in self._inputs:
			result.append("%s " % str(inp))

		result.append(" :output=")
		for out in self._outputs:
			result.append("%s " % str(out))

		result.append(" :params=")
		for para, val in self._params.items():
			result.append("%s:%s " % (para, val))

		return ''.join(result)

	@property
	def name(self):
		return self._filter

	@property
	def inputs(self):
		return self._inputs

	@property
	def outputs(self):
		return self._outputs

	@property
	def params(self):
		return self._params

	def add_input(self, label):
		self._inputs.append(label)
		return self

	def add_output(self, label):
		self._outputs.append(label)
		return self

	def set_inputs(self, inputs):
		self_inputs = inputs
		return self

	def set_outputs(self, outputs):
		self._outputs = outputs
		return

	def __getitem__(self, item):
		return self._outputs[item]


class GlobalNode:
	def __init__(self, inputs=None, args=None, outputs=None):
		self._args = args
		self._inputs = list()
		self._outputs = list()

		if isinstance(inputs, list):
			self._inputs = inputs

		if inputs is not None:
			self._inputs = [inputs]

		if isinstance(outputs, list):
			self._outputs = outputs

		if outputs is not None:
			self._outputs = [outputs]

	def __repr__(self):
		result = list()
		result.append("@global %s :input=" % self._args)

		for inp in self._inputs:
			result.append("%s " % str(inp))

		result.append(" :output=")
		for out in self._outputs:
			result.append("%s " % str(out))

		return ''.join(result)

	@property
	def name(self):
		return self._args

	@property
	def inputs(self):
		return self._inputs

	@property
	def outputs(self):
		return self._outputs

	def add_input(self, label):
		self._inputs.append(label)

	def add_output(self, label):
		self._outputs.append(label)

	def set_inputs(self, inputs):
		self._inputs = inputs
		return self

	def set_outputs(self, outputs):
		self._outputs = outputs
		return self

	def __getitem__(self, item):
		return self._outputs[item]


def stream_operator(stream_classes=None, name=None):
	def decorator(func):
		func_name = name or func.__name__
		[setattr(stream_class, func_name, func) for stream_class in stream_classes]

		return func

	return decorator


def stream():
	return stream_operator(stream_classes=[Label, InputNode, FilterNode, OutputNode, GlobalNode], name=None)
