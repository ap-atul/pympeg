def get_str_from_filter(node):
	result = list()

	for inp in node.inputs:
		result.append(inp)

	result.append("%s=" % node.filter)

	for arg, val in node.params.items():
		result.append("%s:%s" % (arg, val))
	
	for out in node.outputs:
		result.append(out)

	result.append("; ")

	return ''.join(result)

def get_str_from_input(node):
	result = list()
	result.append(" -i %s " % node.params)
	
	return ''.join(result)

def get_str_from_output(node):
	result = list()
	result.append(" %s" % node.params)

	return ''.join(result)
