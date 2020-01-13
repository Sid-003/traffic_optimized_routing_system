from astar import astar
from node import Node, Graph
from roads import Road
from runner import random_nodes, node_reset, segment_load, total_time
import math

graph = Graph()
graph.add_node(1, (0,1))
graph.add_node(2, (1,0))
graph.add_node(3, (1,2))
graph.add_node(4, (2,1))

graph.add_edge(1, 2, Road(80, 2, math.sqrt(2)))
graph.add_edge(1, 3, Road(80, 2, math.sqrt(2)))
graph.add_edge(2, 1, Road(80, 2, math.sqrt(2)))
graph.add_edge(3, 1, Road(80, 2, math.sqrt(2)))

graph.add_edge(4, 2, Road(80, 2, math.sqrt(2)))
graph.add_edge(4, 3, Road(80, 2, math.sqrt(2)))
graph.add_edge(2, 4, Road(80, 2, math.sqrt(2)))
graph.add_edge(3, 4, Road(80, 2, math.sqrt(2)))

graph.add_edge(2, 3, Road(120, 2, 2))
graph.add_edge(3, 2, Road(120, 2, 2))

for vehichles in range(10):

    start_node, end_node = random_nodes(graph)

    path = list(reversed([x.pos for x in astar(graph, Node(graph.nodes[start_node].id,graph.nodes[start_node].pos),
                                               Node(graph.nodes[end_node].id,graph.nodes[end_node].pos))]))

    segment_load(graph, path)
    node_reset(graph)

print(round(total_time(graph)))
