# Runner
# Additional functions to simplify program operations

# Import Necessary Classes
from node import Node, Graph
from roads import Road
import random


# Create Random Vehicle Trips
def random_nodes(graph):
    start_node = random.randint(0, (len(graph.nodes) - 1))
    end_node = random.randint(0, (len(graph.nodes) - 1))
    while start_node == end_node:
        end_node = random.randint(0, (len(graph.nodes) - 1))
    return [start_node, end_node]


# Return All Nodes to Default Values
def node_reset(graph):
    for count in range(len(graph.nodes)):
        graph.nodes[count].reset()


# Load Vehicles onto the System Based on a Route
def segment_load(graph, path, algorithm, load):
    routes = []

    # Create a List of Nodes Travelled Through
    for count in range(len(path)):
        for x in range(len(graph.nodes)):
            if path[count] == graph.nodes[x].pos:
                routes.append(graph.nodes[x].id)

        # Add Vehicle to Segments Between Travelled Nodes
        if count != 0:
            graph.edges[(routes[count - 1], routes[count])].add_vehicles(algorithm, load)


# Calculate Vehicle Travel Time in a System
def total_time(graph, algorithm):
    time = 0

    # For All Possible Start and End Nodes
    for start_node in range(len(graph.nodes) + 1):
        for end_node in range(len(graph.nodes) + 1):

            # Calculate Total Vehicle Time for Road Segment
            try:
                time += graph.edges[(start_node, end_node)].travel_time(
                    graph.edges[(start_node, end_node)].algorithm_used(algorithm)) * graph.edges[
                            (start_node, end_node)].algorithm_used(algorithm)
            except:
                pass

    return time


# Reset Vehicle Loads to 0
def graph_reset(graph):

    # For All Possible Start and End Nodes
    for start_node in range(len(graph.nodes) + 1):
        for end_node in range(len(graph.nodes) + 1):

            # Reset Segment Vehicle Load to 0
            try:
                graph.edges[(start_node, end_node)].aload = 0
                graph.edges[(start_node, end_node)].bload = 0
            except:
                pass