# Better Navigational Algorithm (BNA)
# Our algorithm that cooperatibely manages traffic routing

# Import Necessary Classes
from node import Graph, Node
from runner import node_reset, segment_load, total_time
import copy


# Connection Class
class Connection:

    # Create Connection Objects to Manage Number of Vehicles that Share Start and End Nodes
    def __init__(self, start_node, end_node, load):
        self.start_node = start_node
        self.end_node = end_node
        self.load = load


# Create List of Connections
def arrange(graph, nodes_list):
    connection_list = []

    # For All Possible Start and End Nodes
    for start_node in range(len(graph.nodes) + 1):
        for end_node in range(len(graph.nodes) + 1):
            if start_node != end_node:
                vehicles = 0

                # Count Number of Vehicles on that Connection
                for x in range(len(nodes_list)):
                    if start_node == nodes_list[x][0] and end_node == nodes_list[x][1]:
                        vehicles += 1

                # Add Connection Object to List
                if vehicles != 0:
                    segment = Connection(start_node, end_node, vehicles)
                    connection_list.append(segment)

    return connection_list


# Calculate the Maximum Number of Vehicles to Occupy the Road System at Free Flow Speed
def critical_load(graph):
    load = 0
    for start_node in range(len(graph.nodes) + 1):
        for end_node in range(len(graph.nodes) + 1):
            try:
                load += graph.edges[(start_node, end_node)].k_C * graph.edges[(start_node, end_node)].segment_distance
            except:
                pass
    return load * .25


# For Vehicles Traveling Between Neighboring Nodes
def simple_journey(graph, connection_list):
    long_journeys = []
    for x in range(len(connection_list)):

        # Add Vehicle Load to Road Segment (Edge) Between Nodes
        try:
            graph.edges[(connection_list[x].start_node,
                         connection_list[x].end_node)].add_vehicles('bna', connection_list[x].load)
        except:
            long_journeys.append(connection_list[x])

    # Return Connections not Between Neighboring Nodes
    return long_journeys


# Calculate All Possible Paths for Remaining Connections
def all_paths(graph, connection_list):
    path_all_index = []

    # For Each Connection, Calculate All Possible Paths
    for x in range(len(connection_list)):
        node_reset(graph)
        path_index = all_paths_helper(graph, graph.nodes[connection_list[x].start_node],
                                      graph.nodes[connection_list[x].end_node], path=[], path_index=[])
        path_all_index.append(path_index)

    return path_all_index


# Calculate All Possible Paths
def all_paths_helper(graph, current_node, end_node, path, path_index):
    current_node.closed = True
    path.append(current_node)

    # Recursively Generate All Possible Paths
    if current_node == end_node:
        path_copy = copy.deepcopy(path)
        path_index.append(path_copy)
    else:
        for node in graph.get_neighbors(current_node):
            if not node.closed:
                all_paths_helper(graph, node, end_node, path, path_index)

    # Reopen Nodes to Recursively Generate Other Path Possibilities
    path.pop()
    current_node.closed = False
    return path_index


# Choose 4 Shortest Routes
def rank_routes(graph, routes_list):
    baseline = total_time(graph, 'bna')
    times = []

    # Calculate Time for One Vehicle on Each Route
    for x in range(len(routes_list)):
        segment_load(graph, routes_list[x], 'bna', 1)
        times.append((routes_list[x], total_time(graph, 'bna') - baseline))
        segment_load(graph, routes_list[x], 'bna', -1)

    # Rank Routes by Time and Return Shortest 4
    routes = [x[0] for x in sorted(times, key=lambda x: x[1])]
    for x in range(4 - len(routes)):
        routes.append(None)
    return routes[0:4]


# Calculate Total Time for all Vehicles in Connection at a given Load Distribution
def calculate_time(graph, routes_list, vehicles):
    baseline = total_time(graph, 'bna')
    valid = True

    # Verify that Vehicles Only Exist on Real Road Segments
    for x in range(4):
        if routes_list[x] is None and vehicles[x] != 0:
            valid = False
            current_time = None

    # Calculate Travel Time
    if valid is True:
        for x in range(4):
            if routes_list[x] is not None:
                segment_load(graph, routes_list[x], 'bna', vehicles[x])
        current_time = total_time(graph, 'bna') - baseline
        for x in range(4):
            if routes_list[x] is not None:
                segment_load(graph, routes_list[x], 'bna', (vehicles[x] * -1))
    return current_time


# Find Optimal Distribution of Vehicle Load Between Routes
def load_distribution(graph, connection_list, path_all_index):
    for x in range(len(connection_list)):
        travel_time = None
        routes_list = rank_routes(graph, path_all_index[x])

        # For All Possible Combinations of Vehicle Load Distribution
        for a_vehicles in range(0, (connection_list[x].load + 1)):

            # If Only One Possible Route, Load Vehicles There
            if routes_list[1] is None:
                route_loads = [connection_list[x].load]
            else:

                for b_vehicles in range(0, (connection_list[x].load - a_vehicles + 1)):
                    for c_vehicles in range(0, (connection_list[x].load - b_vehicles + 1)):
                        for d_vehicles in range(0, (connection_list[x].load - c_vehicles + 1)):

                            # Calculate Total Travel Time
                            if (a_vehicles + b_vehicles + c_vehicles + d_vehicles) == connection_list[x].load:
                                current_time = calculate_time(graph, routes_list,
                                                              vehicles=[a_vehicles, b_vehicles, c_vehicles, d_vehicles])

                                # Determine Optimal Distribution by Comparing Travel Times
                                if current_time is not None:
                                    if travel_time is None:
                                        travel_time = current_time
                                        route_loads = [a_vehicles, b_vehicles, c_vehicles, d_vehicles]
                                    elif current_time <= travel_time:
                                        travel_time = current_time
                                        route_loads = [a_vehicles, b_vehicles, c_vehicles, d_vehicles]

        # Load Vehicles Based on Optimal Distribution
        for x in range(4):
            if routes_list[x] is not None:
                segment_load(graph, routes_list[x], 'bna', route_loads[x])


# Better Navigational Algorithm (BNA)
def bna(graph, nodes_list):
    # Sort Vehicles by Start and End Node
    connection_list = arrange(graph, nodes_list)

    # For High Volume Systems, Simplify Process for Neighboring Nodes
    if len(nodes_list) >= critical_load(graph):
        connection_list = simple_journey(graph, connection_list)

    # Find All Possible Paths
    path_all_index = all_paths(graph, connection_list)

    # Determine Optimal Load Distribution and Load Vehicles
    load_distribution(graph, connection_list, path_all_index)
