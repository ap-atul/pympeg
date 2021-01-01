def get_str_from_params(params: dict):
    result = list()
    keys = list(params.keys())
    length = len(keys)

    result.append("%s=%s" % (keys[0], params[keys[0]]))
    for i in range(1, length):
        result.append(":%s=%s" % (keys[i], params[keys[i]]))

    return ''.join(result)

def get_str_from_filter(node):
	result = list()

	for inp in node.inputs:
		result.append(inp)

	result.append("%s=%s" % (node.name, get_str_from_params(node.params)))

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
