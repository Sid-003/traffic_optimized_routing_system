from node import Node, Graph


open_list = []

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
graph.add_node(1, (0, 0))
graph.add_node(2, (0, 1))
graph.add_node(3, (0, 2))
graph.add_node(4, (1, 1))
graph.add_node(5, (2, 2))
graph.add_node(6, (2, 1))
graph.add_node(7, (2, 0))
graph.add_node(8, (4, 1))
graph.add_node(9, (4, 0))
graph.add_node(10, (5, 0.5))


graph.add_edge(1, 4, 3)
graph.add_edge(2, 4, 3)
graph.add_edge(3, 4, 3)
graph.add_edge(4, 5, 3)
graph.add_edge(4, 6, 3)
graph.add_edge(4, 7, 3)
graph.add_edge(7, 9, 3)
graph.add_edge(6, 8, 3)
graph.add_edge(8, 10, 3)


print(list(reversed([x.pos for x in astar(graph, Node(5, (2, 2)), Node(10, (5, 0.5)))])))