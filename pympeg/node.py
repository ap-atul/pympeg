from pympeg.exceptions import FilterParamsMissing, FileNameMissing


class IONode:
	def __init__(self, name=None):
		self._file = name

		if name is None:
			raise FileNameMissing

	@property
	def params(self):
		return self._file

	def __str__(self):
		return '@ionode %s' % self._file


class FilterNode:
	def __init__(self, inputs=None, outputs=None, filter_name=None, params=None):
		self._filter_name = filter_name
		self._params = params
		self._inputs = list()
		self._outputs = list()

		# not allowing empty labels
		if inputs == None or outputs == None:
			raise FilterParamsMissing

		# adding input links
		if isinstance(inputs, list):
			for inp in inputs:
				self._inputs.append("[%s]" % inp)
		else:
			self._inputs.append("[%s]" % inputs)

		# adding output linsk
		if isinstance(outputs, list):
			for out in outputs:
				self._outputs.append("[%s]" % out)
		else:
			self._outputs.append("[%s]" % outputs)

	def __str__(self):
		return "@filternode %s : i=%d : o=%d : in = %s : out = %s" % (self._filter_name, len(self._inputs) , len(self._outputs), self._inputs, self._outputs)

	@property
	def name(self):
		return self._filter_name

	@property
	def inputs(self):
		return self._inputs

	@property
	def outputs(self):
		return self._outputs

	@property
	def params(self):
		return self._params

