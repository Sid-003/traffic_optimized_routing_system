from astar import astar
from bna import bna
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


num = 10
nodes_list = [[0,1],[0,3]]
# for vehichles in range(num):
 #  nodes_list.append(random_nodes(graph))

bna(graph, nodes_list)
input()

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
#nodes_list = order(graph, nodes_list)
#for vehichles in range(num):

    #start_node = nodes_list[vehichles][0]
    #end_node = nodes_list[vehichles][1]

    path = list(reversed([x.pos for x in bna(graph, Node(graph.nodes[start_node].id, graph.nodes[start_node].pos),
                                               Node(graph.nodes[end_node].id, graph.nodes[end_node].pos))]))
    segment_load(graph, path, 'bna')
    node_reset(graph)

print(round(total_time(graph, 'astar')))
print(round(total_time(graph, 'bna')))