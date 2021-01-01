class FilterParamsMissing(Exception):
	""" 
	When some parameters are missing while initializing the Filter Node.
	This exception will be raised asking for the completion of the missing
	parameters
	"""
	def __str__(self):
		return "Filter node has missing arguments. Use " \
				"""filter = FilterNode([in], [out], trim, {"start": 3, "duration": 4}) """

class FileNameMissing(Exception):
	"""
	When name of the file is missing while initilization of the IONode.
	This exception will be raised asking for the missing name of the file.
	The file should be complete address not only the name of the file
	"""
	def __str__(self):
		return "File name is missing for the IONode. Use" \
			""" input_node = IONode("/home/user/a.mp4") """

