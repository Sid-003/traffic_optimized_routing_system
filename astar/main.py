from astar import astar
from node import Node, Graph
from roads import Road

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


graph.add_edge(1, 4, Road(5, 2, 2))
graph.add_edge(1, 2, Road(30, 2, 2))
graph.add_edge(2, 4, Road(120, 2, 3.5))
graph.add_edge(3, 4, Road(120, 2, 2))
graph.add_edge(4, 5, Road(120, 2, 2))
graph.add_edge(4, 6, Road(120, 2, 6.9))
graph.add_edge(4, 7, Road(120, 2, 4.20))
graph.add_edge(7, 9, Road(120, 2, 2))
graph.add_edge(6, 8, Road(120, 2, 2))
graph.add_edge(8, 10, Road(120, 2, 2))
graph.add_edge(4, 3, Road(120, 2, 2))
graph.add_edge(4, 1, Road(120, 2, 2))
graph.add_edge(2, 1, Road(120, 2, 2))
graph.add_edge(4, 2, Road(120, 2, 2))
graph.add_edge(5, 4, Road(120, 2, 2))
graph.add_edge(6, 4, Road(120, 2, 6.9))
graph.add_edge(7, 4, Road(120, 2, 4.20))
graph.add_edge(9, 7, Road(120, 2, 2))
graph.add_edge(8, 6, Road(120, 2, 2))
graph.add_edge(10, 8, Road(120, 2, 2))

print(list(reversed([x.pos for x in astar(graph, Node(1, (0, 0)), Node(5, (2, 2)))])))