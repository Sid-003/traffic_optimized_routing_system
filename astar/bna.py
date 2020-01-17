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
            graph.edges[((connection_list[x].start_node + 1),
                         (connection_list[x].end_node + 1))].add_vehichle('bna',connection_list[x].load)
        except:
            long_journeys.append(connection_list[x])
    return long_journeys


def all_paths(graph, connection_list):
    path_all_index = []

    for x in range(len(connection_list)):
        node_reset(graph)
        path_index = all_paths_helper(graph, graph.nodes[connection_list[x].start_node],
                                      graph.nodes[connection_list[x].end_node], path=[], path_index=[])
        path_all_index.append(path_index)

    return path_all_index


# to fix: repeat node error
# to add: limit on too long paths
def all_paths_helper(graph, current_node, end_node, path, path_index):
    current_node.closed = True
    path.append(current_node)

    if current_node == end_node:
        """
        for x in range(len(path)):
            print(path[x].id)
        print()
        """
        path_copy = copy.deepcopy(path)
        path_index.append(path_copy)
    else:
        for node in graph.get_neighbors(current_node):
            if not node.closed:
                all_paths_helper(graph, node, end_node, path, path_index)

    path.pop()
    current_node.closed = False
    return path_index


def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset + 1)
        except ValueError:
            return result
        result.append(offset)


def rank_routes(graph, routes_list):
    baseline = total_time(graph, 'bna')
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
    sorted_times = sorted(times)[0:4]

    new_routes_list = []
    used_times = []
    for count in range(4):
        if sorted_times[count] is not None:
            used = False
            for x in range(len(used_times)):
                if sorted_times[count] == used_times[x]:
                    used = True
            if used is True:
                break
            indexes = indices(times, sorted_times[x])
            for x in range(len(indexes)):
                new_routes_list.append(routes_list[indexes[x]])

    for x in range(4):
        try:
            new_routes_list[x]
        except:
            new_routes_list.append(None)
    return new_routes_list


def calculate_time(graph, routes_list, vehicles):
    baseline = total_time(graph, 'bna')
    for x in range(4):
        if routes_list[x] is not None:
            segment_load(graph, routes_list[x], 'bna', vehicles[x])
    curent_time = total_time(graph, 'bna') - baseline
    for x in range(4):
        if routes_list[x] is not None:
            segment_load(graph, routes_list[x], 'bna', (vehicles[x] * -1))
    return curent_time


def load_distribution(graph, connection_list, path_all_index):
    for x in range(len(connection_list)):
        travel_time = None
        routes_list = rank_routes(graph, path_all_index[x])

        for a_vehicles in range(0, (connection_list[x].load + 1)):
            if routes_list[1] is None:
                segment_load(graph, path_all_index[x][0], 'bna', connection_list[x].load)
            else:
                for b_vehicles in range(0, (connection_list[x].load - a_vehicles + 1)):
                    for c_vehicles in range(0, (connection_list[x].load - b_vehicles + 1)):
                        for d_vehicles in range(0, (connection_list[x].load - c_vehicles + 1)):

                            if (a_vehicles + b_vehicles + c_vehicles + d_vehicles) == connection_list[x].load:
                                current_time = calculate_time(graph, routes_list,
                                                              vehicles=[a_vehicles, b_vehicles, c_vehicles, d_vehicles])
                                if travel_time is None:
                                    travel_time = current_time
                                    route_loads = [a_vehicles, b_vehicles, c_vehicles, d_vehicles]
                                elif current_time <= travel_time:
                                    travel_time = current_time
                                    route_loads = [a_vehicles, b_vehicles, c_vehicles, d_vehicles]

        for x in range(4):
            segment_load(graph, routes_list[x], 'bna', route_loads[x])

            """
            for y in range(len(routes_list[x])):
                print(routes_list[x][y].id)
            print(route_loads[x])
            print()
            """


def bna(graph, nodes_list):
    connection_list = arrange(graph, nodes_list)
    connection_list = simple_journey(graph, connection_list)
    path_all_index = all_paths(graph, connection_list)
    load_distribution(graph, connection_list, path_all_index)
