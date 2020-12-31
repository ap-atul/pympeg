""" Stream will manage the graph and node interactions """

from pympeg._node import *


class Stream(Node):
	def __init__(self):
		super().__init__()
		
		self._sources = list()
		self._sink = None

	def input(self, name):
		node = IONode(name=name)
		self._sources.append(node)
		return node

	def filter(self, input_node=None, **kwargs):
		inp = input_node

		if inp in self._sources:
			node = FilterNode(**kwargs).set_input_label("%s" % self._sources.index(inp))
		else:
			node = FilterNode(**kwargs).set_input_label("%s" % inp.out_label)

		return self


if __name__ == "__main__":
	s = Stream()
	node = s.input("input.mp4")
	s.filter(node, filter_name="trim", params={"st":2, "d":3})
	

