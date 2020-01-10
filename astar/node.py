class Graph:

    def __init__(self):
        self.nodes = []
        self.edges = {}

    def add_node(self, id, pos):
        self.nodes.append(Node(id, pos))

    def add_edge(self, e1, e2, c):
        self.edges[(e1, e2)] = c

    def get_neighbors(self, node):
        final = []
        for x in list(self.edges.keys()):
            if x[0] == node.id:
                final.append(self.nodes[x[1] -1])
            elif x[1] == node.id:
                if not(x in final):
                    final.append(self.nodes[x[0] - 1])
        return final

    def get_cost(self, current, neighbor):
        #just uses the distance currently
        return 1


class Node:

    def __init__(self, id, position=None, parent=None):
        self.id = id
        self.g = None
        self.h = 0
        self.f = 0
        self.parent = parent
        self.pos = position
        self.closed = False

    def __eq__(self, other):
        return self.pos == other
