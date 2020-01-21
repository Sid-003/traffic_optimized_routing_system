from node import Node, Graph
from roads import Road
import random

def random_nodes(graph):
    start_node = random.randint(0, (len(graph.nodes) - 1))
    end_node = random.randint(0, (len(graph.nodes) - 1))
    while start_node == end_node:
        end_node = random.randint(0, (len(graph.nodes) - 1))
    return [start_node, end_node]

def node_reset(graph):
    for count in range(len(graph.nodes)):
        graph.nodes[count].reset()

def segment_load(graph, path, algorithm, load):
    routes = []
    for count in range(len(path)):
        for x in range(len(graph.nodes)):
            if path[count] == graph.nodes[x].pos:
                routes.append(graph.nodes[x].id)
        if count != 0:
            graph.edges[(routes[count - 1], routes[count])].add_vehichle(algorithm, load)

def total_time(graph, algorithm):
    time = 0
    for start_node in range(len(graph.nodes) + 1):
        for end_node in range(len(graph.nodes) + 1):
            try:
                time += graph.edges[(start_node, end_node)].travel_time(graph.edges[(start_node, end_node)].algorithm_used(algorithm)) * graph.edges[
                    (start_node, end_node)].algorithm_used(algorithm)
            except:
                pass
    return time


def total_load(graph, algorithm):
    load = 0
    for start_node in range(len(graph.nodes) + 1):
        for end_node in range(len(graph.nodes) + 1):
            try:
                load += graph.edges[(start_node, end_node)].algorithm_used(algorithm)
            except:
                pass
    return load
