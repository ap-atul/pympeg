""" Builder to build the node chain """
from ._util import *
from ._node import *

def get_str_from_params(params: dict):
    """ Returns string from the parameters """
    result = list()
    keys = list(params.keys())
    length = len(keys)

    result.append("%s=%s" % (keys[0], params[keys[0]]))
    for i in range(1, length):
        result.append(":%s=%s" % (keys[i], params[keys[i]]))

    return ''.join(result)


def get_str_from_filter(filter):
    """ Returns the string from the filter """
    result = list()

    for inp in filter.inputs:
        result.append("[%s]" % inp.label)

    result.append(" %s=%s " % (filter.name, get_str_from_params(filter.params)))

    for out in filter.outputs:
        result.append("[%s]" % out.label)

    result.append(";")

    return ''.join(result)


def get_str_from_global(node):
    """ Returns the string from the global node """
    result = list()

    for inp in node.inputs:
        result.append("[%s]" % inp.label)

    result.append("%s" % node.name)

    for out in node.outputs:
        result.append("[%s]" % out.label)

    result.append(";")

    return ''.join(result)


def get_str_from_input(node):
    result = list()
    result.append("-i %s" % node.name)
    return ' '.join(result)


def get_str_from_output(node):
    result = list()
    for inp in node.inputs:
        result.append('%s "[%s]"' % (node.map, inp.label))
    result.append(" %s " % node.name)
    return ' '.join(result)


def get_str_from_option(node):
    result = list()
    result.append(" %s %s" % (node.tag, node.name))
    return ' '.join(result)

def get_str_from_node(node):
    if isinstance(node, InputNode):
        return get_str_from_input(node)
    if isinstance(node, OptionNode):
        return get_str_from_option(node)
    if isinstance(node, FilterNode):
        return get_str_from_filter(node)
    if isinstance(node, GlobalNode):
        return get_str_from_global(node)
    if isinstance(node, OutputNode):
        return get_str_from_output(node)


class Stream:
    """
    Simple list manager, adds nodes and returns the chain
    of graph call. Also keeps track of labelling the input
    nodes.
    """
    def __init__(self):
        self._chain, self.count = list(), 0
    def add(self, data):
        self._chain.append(data)
        return self
    def graph(self):
        return self._chain

class Stringify:
    @staticmethod
    def get_command_from_graph(nodes, cmd='ffmpeg'):  # nodes is a list 
        command = list()
        command.append(cmd)
        filter_cnt = 0

        for node in nodes:
            if isinstance(node, FilterNode):
                if filter_cnt == 0:
                    command.append('-filter_complex "')
                else:
                    command.append(';')
            if isinstance(node, OutputNode):
                last = command.pop()
                command.append(last.replace(";", ""))
            command.append(get_str_from_node(node))

        return ' '.join(command)
