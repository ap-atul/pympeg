""" Builder to build the node chain """
from ._util import *
from ._node import *

class Stream:
    """
    Simple list manager, adds nodes and returns the chain
    of graph call. Also keeps track of labelling the input
    nodes.
    """
    def __init__(self):
        self._chain = list()
    def add(self, data):
        self._chain.append(data)
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
