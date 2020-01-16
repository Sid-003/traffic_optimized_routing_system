# BNA
# Better Navigational Algorithm

from node import Graph, Node
from runner import node_reset, segment_load, total_time
import copy


class connection:

    def __init__(self, start_node, end_node, load):
        self.start_node = start_node
        self.end_node = end_node
        self.load = load


def arrange(graph, nodes_list):
    connection_list = []
    for start_node in range(len(graph.nodes) + 1):
        for end_node in range(len(graph.nodes) + 1):
            if start_node != end_node:
                vehichles = 0
                for x in range(len(nodes_list)):
                    if start_node == nodes_list[x][0] and end_node == nodes_list[x][1]:
                        vehichles += 1
                if vehichles != 0:
                    segment = connection(start_node, end_node, vehichles)
                    connection_list.append(segment)
    return connection_list


def simple_journey(graph, connection_list):
    long_journeys = []
    for x in range(len(connection_list)):
        try:
            graph.edges[((connection_list[x].start_node + 1), (connection_list[x].end_node + 1))].add_vehichle('bna', connection_list[x].load)
        except:
            long_journeys.append(connection_list[x])
    return long_journeys


def all_paths(graph, connection_list):
    path_all_index = []

    for x in range(len(connection_list)):
        node_reset(graph)
        path_index = all_paths_helper(graph,
                               Node(graph.nodes[connection_list[x].start_node].id,
                                    graph.nodes[connection_list[x].start_node].pos),
                               Node(graph.nodes[connection_list[x].end_node].id,
                                    graph.nodes[connection_list[x].end_node].pos), path=[], path_index=[])
        path_all_index.append(path_index)

    return path_all_index


# to fix: repeat node error
# to add: limit on too long paths
def all_paths_helper(graph, current_node, end_node, path, path_index):
    current_node.closed = True
    path.append(current_node)

    if current_node == end_node:
        path_copy = copy.deepcopy(path)
        path_index.append(path_copy)
    else:
        for node in graph.get_neighbors(current_node):
            if not node.closed:
                all_paths_helper(graph, node, end_node, path, path_index)

    path.pop()
    current_node.closed = False
    return path_index


def rank_routes(graph, routes_list):
    baseline =  total_time(graph, 'bna')
    times = []

    for x in range(len(routes_list)):
        segment_load(graph, routes_list[x], 'bna', 1)
        times.append(total_time(graph, 'bna') - baseline)
        segment_load(graph, routes_list[x], 'bna', -1)

    for x in range(4):
        try:
            times[x]
        except:
            times.append(None)

    return sorted(times)[0:4]
        

def bna(graph, nodes_list):
    connection_list = arrange(graph, nodes_list)
    connection_list = simple_journey(graph, connection_list)
    path_all_index = all_paths(graph, connection_list)

    for x in range(len(connection_list)):
        travel_time = None

        routes_list = rank_routes(graph, path_all_index[x])
        print(routes_list)

        for a_vehicles in range(0,connection_list[x].load):
            if routes_list[1] is None:
                segment_load(graph, path_all_index[x][0], 'bna', connection_list[x].load)
            else:
                for b_vehicles in range(0,connection_list[x].load - a_vehicles):
                    for c_vehicles in range(0,connection_list[x].load - b_vehicles):
                        for d_vehicles in range(0, connection_list[x].load - c_vehicles):
                            if



"""
        route_optimal_load = []
        for count in range(len(path_all_index[x])):
            route_optimal_load.append(0)

        for count in range(len(path_all_index[x])):



            # error
            for vehichles in range(connection_list[x].load + 1):
                segment_load(graph, path_all_index[x][count], 'bna', vehichles)

            current_time = total_time(graph, 'bna')
            if current_time < travel_time or travel_time is None:
                travel_time = current_time
                for y in range(len(path_all_index[x])):
                    segment_partial_load[y] =
"""
    # add optimization of path loads


