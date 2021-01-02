class FilterParamsMissing(Exception):
	"""
	When some parameters are missing while initializing the Filter Node,
	this exception will be raised asking for the completion of the missing
	parameters
	"""

	def __str__(self):
		return "Filter node has missing arguments. \n Use like :: " \
			   """filter(filter_name="trim", params={"start": 10, "duration": 20})"""


class FileNameMissing(Exception):
	"""
	When name of the file is missing while initialization of the IONode,
	this exception will be raised asking for the missing name of the file.
	The file should be complete address not only the name of the file
	"""

	def __str__(self):
		return "File name is missing for the IONode. \n Use like :: " \
			   """ pympeg.input(name="example.mp4") """


class TypeMissing(Exception):
	"""
	When the type of the node is missing from the important functions, this
	exception will be raised along with the message
	"""
	pass


class ProbeException(Exception):
	"""
	When the probe function runs into some error this exception would be raised,
	along with the command line output what so ever.
	"""
	pass
