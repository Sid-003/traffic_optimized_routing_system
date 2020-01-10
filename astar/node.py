from roads import Road


class Graph:

    def __init__(self):
        self.nodes = []
        self.edges = {}

    def add_node(self, id, pos):
        self.nodes.append(Node(id, pos))

    def add_edge(self, e1, e2, c):
        self.edges[(e1, e2)] = c

    def get_neighbors(self, node):
        return [x for x in self.edges if node.id == x[1]]

    def get_cost(self, current, neighbor):
        road:Road = self.edges[(current.id, neighbor.id)]
        return road.travel_time(0)


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
