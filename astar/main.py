from astar import astar
from bna import bna
from node import Node, Graph
from roads import Road
from runner import random_nodes, node_reset, segment_load, total_time, total_load
import math

graph = Graph()
graph.add_node(0, (0, 1))
graph.add_node(1, (1, 0))
graph.add_node(2, (4, 3))
graph.add_node(3, (5, 2))

graph.add_edge(0, 1, Road(120, 1, math.sqrt(2)))
graph.add_edge(2, 3, Road(120, 1, math.sqrt(2)))
graph.add_edge(1, 0, Road(120, 1, math.sqrt(2)))
graph.add_edge(3, 2, Road(120, 1, math.sqrt(2)))

graph.add_edge(1, 3, Road(60, 4, math.sqrt(13)))
graph.add_edge(0, 2, Road(60, 4, math.sqrt(13)))
graph.add_edge(3, 1, Road(60, 4, math.sqrt(13)))
graph.add_edge(2, 0, Road(60, 4, math.sqrt(13)))

graph.add_edge(1, 2, Road(120, 4, math.sqrt(13)))
graph.add_edge(2, 1, Road(120, 4, math.sqrt(13)))


num = 500
nodes_list = []
for vehichles in range(num):
    nodes_list.append(random_nodes(graph))

# astar
for vehichles in range(num):

    #start_node, end_node = random_nodes(graph)
    start_node = nodes_list[vehichles][0]
    end_node = nodes_list[vehichles][1]

    path = list(reversed([x.pos for x in astar(graph, Node(graph.nodes[start_node].id,graph.nodes[start_node].pos),
                                               Node(graph.nodes[end_node].id,graph.nodes[end_node].pos))]))
    segment_load(graph, path, 'astar', 1)
    node_reset(graph)

# bna
bna(graph, nodes_list)

print(round(total_time(graph, 'astar')))
print(round(total_time(graph, 'bna')))
print()