# Main

# Import Necessary Classes and Functions
from astar import astar
from bna import bna
from node import Node, Graph
from roads import Road
from runner import random_nodes, node_reset, segment_load, total_time, graph_reset
import math, random

# Create a Graph Object
graph = Graph()

# List Nodes in Graph
graph.add_node(0, (0, 1))
graph.add_node(1, (1, 0))
graph.add_node(2, (4, 3))
graph.add_node(3, (5, 2))

# List Edges Between Nodes in Graph
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

num = 710
for x in range(30):
    num -= 10

    # Create List of Randomized Vehicle Trips
    nodes_list = []
    for vehicles in range(num):
        nodes_list.append(random_nodes(graph))

    # Run A* Algorithm for Every Vehicle
    for vehicles in range(num):

        # Find Start and End Nodes from list
        start_node = nodes_list[vehicles][0]
        end_node = nodes_list[vehicles][1]

        # Find Ideal Shortest Path using A* to Minimize Travel Time
        path = list(reversed([x.pos for x in astar(graph, Node(graph.nodes[start_node].id,graph.nodes[start_node].pos),
                                                   Node(graph.nodes[end_node].id,graph.nodes[end_node].pos))]))

        # Load Vehicle into Traffic System
        segment_load(graph, path, 'astar', 1)

        # Reset All Nodes to Default Values
        node_reset(graph)

    # Run Better Navigational Algorithm (BNA)
    bna(graph, nodes_list)

    file = open("astar_times.txt","a")
    file.write(str(total_time(graph, 'astar')) + '\n')
    file.close()

    file = open("bna_times.txt", "a")
    file.write(str(total_time(graph, 'bna')) + '\n')
    file.close()

    file = open("vehicles.txt", "a")
    file.write(str(num) + '\n')
    file.close()

    graph_reset(graph)
    print(num)
