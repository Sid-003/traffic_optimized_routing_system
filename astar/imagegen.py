import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

from node import Graph
from roads import Road


def calculate_shift(dx, dy):
    tf = (0, 0)
    o = 'l'
    s = 0.05
    if dx != 0:
        slope = dy / dx
        if slope > 0.0:
            if dy > 0:
                tf = (-1 * s, s)
                o = 'r'
            else:
                tf = (s, -1 * s)
        elif slope < 0.0:
            if dy < 0:
                tf = (s, s)
                o = 'r'
            else:
                tf = (-1 * s, -1 * s)
        else:
            if dx > 0:
                tf = (0, s)
                o = 'r'
            else:
                tf = (0, -1 * s)
    else:
        if dy > 0:
            tf = (-1 * s, 0)
        else:
            tf = (s, 0)

    return o, tf


def generate_image(g: Graph, best_path):
    cf = plt.gcf()

    ax = cf.add_axes((0, 0, 1, 1))
    ax.set_facecolor((0, 0, 0))
    nodes = g.nodes
    edges = g.edges.keys()

    xy = np.asarray([x.pos for x in nodes])

    ax.scatter(xy[:, 0], xy[:, 1], s=500, c='white', edgecolors=['red'], linewidths=2)

    best_edges = []
    normal_edges = []

    for e in edges:
        p1 = nodes[e[0] - 1].pos
        p2 = nodes[e[1] - 1].pos

        (x1, y1) = p1
        (x2, y2) = p2
        dx = x2 - x1
        dy = y2 - y1
        t = calculate_shift(dx, dy)
        tf = t[1]

        if (t[0] == 'r'):
            label = str(round(g.edges[e].travel_time(0), 2)) + '--->'
        else:
            label = '<---' +  str(round(g.edges[e].travel_time(0), 2))

        (x, y) = ((0.5 * (x1 + x2)) + tf[0], (0.5 * (y1 + y2)) + tf[1])

        angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
        if angle > 90:
            angle -= 180
        if angle < - 90:
            angle += 180

        xy = np.array((x, y))
        trans_angle = ax.transData.transform_angles(np.array((angle,)),
                                                    xy.reshape((1, 2)))[0]

        ax.text(x, y, label, size=10, color='yellow', horizontalalignment='center', verticalalignment='center',
                rotation=trans_angle,
                zorder=5)
        # Add to different collections based on the best path.
        if p1 in best_path and p2 in best_path:
            best_edges.append((p1, p2))
        else:
            normal_edges.append((p1, p2))
    ne = np.asarray(normal_edges)
    be = np.asarray(best_edges)
    edge_collection = LineCollection(ne, colors='white')
    best_path_edge_collection = LineCollection(be, colors='green')
    edge_collection.set_zorder(-69)
    best_path_edge_collection.set_zorder(-69)
    ax.add_collection(edge_collection)
    ax.add_collection(best_path_edge_collection)
    for node in nodes:
        (x, y) = node.pos
        ax.text(x, y, str(node.id), size=15, horizontalalignment='center', verticalalignment='center')

    return plt
