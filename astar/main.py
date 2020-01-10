from node import Node, Graph


open_list = []
closed_list = []

# Direction:    N       S       E        W        NE       SW       NW        SE
directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

def is_valid(pos):
    return True


def calculate_heuristics(current_node, successor):
    (x1, y1) = current_node.pos
    (x2, y2) = successor.pos
    dx = (x2 - x1) ** 2
    dy = (y2 - y1) ** 2
    return dx + dy


def build_path(current_node: Node):
    path = [current_node]
    while current_node.parent is not None:
        parent = current_node.parent
        path.append(parent)
        current_node = parent
    return path


def astar(graph: Graph, start_node, end_node):
    open_list.append(start_node)
    start_node.g = 0
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
            tentativeG = current_node.g + calculate_heuristics(current_node, neighbor)
            if neighbor.g is None or tentativeG < neighbor.g:
                neighbor.parent = current_node
                neighbor.g = tentativeG
                neighbor.h = calculate_heuristics(current_node, end_node)
                neighbor.f = neighbor.g + neighbor.h
                if not(neighbor in open_list):
                    open_list.append(neighbor)

graph = Graph()
graph.generate_nodes()
graph.generate_connections()

print(list(reversed([x.pos for x in astar(graph, Node(7, (3, 2)), Node(4, (1, 0)))])))