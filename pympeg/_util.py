from random import sample
import string


def gen_label(length=5):
    return ''.join(sample(string.ascii_letters, length))


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
    result.append("%s %s=%s %s;" % (node.inputs, node.filter, get_str_from_params(node.params), node.outputs))

    return ' '.join(result)


def get_str_from_ionode(node):
    result = list()
    result.append("-i %s" % node.params)
    return ' '.join(result)


def get_str_from_graph(graph):
    result = list()
    output = graph.pop()

    result.append("ffmpeg -y")
    result.append("-i %s" % graph.pop(0).params)
    result.append('-filter_complex"')
    for node in graph:
        result.append(get_str_from_filter(node))
    result.append('"')
    result.append("%s" % output.params)

    return " ".join(result)
