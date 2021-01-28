""" Builder to build the node chain """

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
