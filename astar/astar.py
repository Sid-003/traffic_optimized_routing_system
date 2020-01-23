# A* Path-Finding Algorithm
# This algorithm is equivalent to those currently used by GPS Navigation tools, like Google Maps

# Import Nodes and Graph classes
from node import Graph, Node


# Determine Optimal Direction from Current Location to End
def calculate_heuristics(current_node, other_node):

    # Utilize Euclidian Distance
    (x1, y1) = current_node.pos
    (x2, y2) = other_node.pos
    dx = (x2 - x1) ** 2
    dy = (y2 - y1) ** 2
    return dx + dy


# Add Node to Ideal Shortest Path
def build_path(current_node: Node):
    path = [current_node]
    while current_node.parent is not None:
        parent = current_node.parent
        path.append(parent)
        current_node = parent
    return path


# A* Algorithm
def astar(graph: Graph, start_node, end_node):
    start_node.g = 0
    open_list = [start_node]
    while len(open_list) > 0:
        current_node = open_list[0]

        for node in open_list:
            if node.f < current_node.f:
                current_node = node

        if current_node == end_node:
            return build_path(current_node)

        open_list.remove(current_node)
        current_node.closed = True
        for neighbor in graph.get_neighbors(current_node):
            if neighbor.closed:
                continue
            tentativeG = current_node.g + graph.get_cost(current_node, neighbor, 'astar')
            if neighbor.g is None or tentativeG < neighbor.g:
                neighbor.parent = current_node
                neighbor.g = tentativeG
                neighbor.h = calculate_heuristics(current_node, end_node)
                neighbor.f = neighbor.g + neighbor.h
                if not (neighbor in open_list):
                    open_list.append(neighbor)