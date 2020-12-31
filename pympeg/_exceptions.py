class InputOutputFileMissingException(Exception):
	"""
	When the input and output noded does not have any file name
	assigned this exception would be raised. The IONode should
	have the name of the file to process or output
	"""
	def __str__(self):
		return "Input and Ouput should have the name of the file."


class FilterNameMissingException(Exception):
	""" 
	When the filter node does not have any filter name this exception
	would be raised. Every filter node must contain the filter name
	for building the command line to run 
	"""
	def __str__(self):
		return "Filter requires the name of the filter, try using predefined filters."


class FilterParamsMissingException(Exception):
	"""
	When the filter node does not contain any parameters then this
	exception would be raise. Every filter node must have atleast one
	parameter to run the filter
	"""
	def __str__(self):
		return "Filter requires at least one parameters, try using predefined."
