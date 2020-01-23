# Traffic System Graph Tools
# Provides ability to create nodes and edges to simulate a traffic system

# Import Roads Class
from roads import Road


# Graph Class
class Graph:

    # Cretae Nodes and Edges
    def __init__(self):
        self.nodes = []
        self.edges = {}

    # Add Node to Graph
    def add_node(self, id, pos):
        self.nodes.append(Node(id, pos))

    # Add Edge Between Two Nodes
    def add_edge(self, e1, e2, c):
        self.edges[(e1, e2)] = c

    # Return Nodes Connected to Given Node by Edges
    def get_neighbors(self, node):
        return [self.nodes[x[1]] for x in self.edges.keys() if node.id == x[0]]

    # Return Speed of Traffic on Edge
    def get_cost(self, current, neighbor, algorithm):
        road: Road = self.edges[(current.id, neighbor.id)]
        return road.travel_time(road.algorithm_used(algorithm))


# Node Class
class Node:

    # Node Attributions
    def __init__(self, id, position=None, parent=None):
        self.id = id
        self.g = None
        self.h = 0
        self.f = 0
        self.parent = parent
        self.pos = position
        self.closed = False

    # Implement Equality so that Nodes are Comparable
    def __eq__(self, other):
        return self.pos == other

    # String Representation of Node (Debugging)
    def __st__(self):
        return "Id: {0}, Position: {1}".format(self.id, self.pos)

    # Reset Node Attributions to Default Values
    def reset(self):
        self.g = None
        self.h = 0
        self.f = 0
        self.parent = None
        self.closed = False