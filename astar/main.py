# Main

# Import Necessary Classes and Functions
from PIL import Image, ImageDraw
from matplotlib.figure import Figure

from astar import astar
from bna import bna
from imagegen import composite_and_save, generate_image
from node import Node, Graph
from roads import Road
from runner import random_nodes, node_reset, segment_load, total_time, graph_reset
import math, random
import matplotlib.pyplot as plt
import matplotlib.image as imgr

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

# Run Both Algorithms Once with 500 vehicles
num = 510
for x in range(1):
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
        path = list(reversed([x.pos for x in astar(graph, Node(graph.nodes[start_node].id, graph.nodes[start_node].pos),
                                                   Node(graph.nodes[end_node].id, graph.nodes[end_node].pos))]))

        # Load Vehicle into Traffic System
        segment_load(graph, path, 'astar', 1)

        # Reset All Nodes to Default Values
        node_reset(graph)

    # Run Better Navigational Algorithm (BNA)
    bna(graph, nodes_list)

    # Generate the two images and save it.
    m1 = generate_image(graph, 'astar')
    m2 = generate_image(graph, 'bna')
    composite_and_save(m1, m2)

    # Display the image.
    img:Image = Image.open('graph.png')
    img.show()

    # Reset the graph.
    graph_reset(graph)

