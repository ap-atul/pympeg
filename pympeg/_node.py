""" 
Node classes that acts as a start -> intermediate -> output nodes in the filter graph, 
each node may contain set of arguments and labels (input and output)
"""

from pympeg._exceptions import *
from pympeg._util import gen_label
from pympeg._graph import Graph


class Node(object):
	""" Used to create labels and identify each node """
	
	def __init__(self):
		self._in_label = "[%s]" % gen_label()
		self._out_label = "[%s]" % gen_label()

	@property
	def out_label(self):
		return self._out_label

	@property
	def in_label(self):
		return self._in_label


class IONode(Node):
	""" Independant node """
	
	def __init__(self, name=None):
		super().__init__()
		if name is None or not isinstance(name, str):
			raise InputOutputFileMissingException

		self._name = name

	def __str__(self):
		return " file: %s " % self._name

	@property
	def params(self):
		return self._name
	
	def set_output_label(self, label):
		self._in_label = label
		return self


class FilterNode(Node):
	""" Every filter will consists of a input and output label """
	
	def __init__(self, filter_name=None, params=None, inputs=1, outputs=1):
		super().__init__()

		# checking for filter name and its type
		if filter_name is None or not isinstance(filter_name, str):
			raise FilterNameMissingException

		# checking for filter parameters and its type
		if params is None or not isinstance(params, dict):
			raise FilterParamsMissingException

		self._filter_name = filter_name
		self._params = params
		self._inputs = inputs
		self._outputs = outputs

	def __str__(self):
		return "  %s (%s, %s )  " % (self._filter_name, self.in_label, self.out_label)
		
	@property
	def filter(self):
		return self._filter_name

	@property
	def params(self):
		return self._params

	@property
	def outputs(self):
		return [FilterNode(self._filter_name, self.params).set_input_label(self.out_label) for _ in range(self._outputs)]

	def set_filter_name(self, filter_name):
		self._filter_name = filter_name
		return self

	def set_params(self, params):
		self._params = params
		return self

	def set_input_label(self, label):
		self._in_label = label
		return self

	def set_output_label(self, label):
		self._out_label = label
		return self

	def set_inputs(self, inputs):
		self._inputs = inputs
		return self

	def set_outputs(self, outputs):
		self._outputs = outputs
		return self

