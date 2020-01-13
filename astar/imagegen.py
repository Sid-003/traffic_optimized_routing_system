import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection

from node import Graph

def generate_image(g: Graph):
    cf = plt.gcf()

    ax = cf.add_axes((0, 0, 1, 1))
    ax.set_facecolor((0, 0, 0))
    nodes = g.nodes
    edges = g.edges.keys()

    xy = np.asarray([x.pos for x in nodes])

    ax.scatter(xy[:, 0], xy[:, 1], s = 500, c = 'white', edgecolors=['red'], linewidths = 2)

    e = np.asarray([(nodes[e[0]-1].pos, nodes[e[1]-1].pos) for e in edges])
    edge_collection =  LineCollection(e, colors='white')
    ax.add_collection(edge_collection)
    for node in nodes:
        (x, y) = node.pos
        ax.text(x, y, str(node.id), size = 15, horizontalalignment = 'center', verticalalignment='center')

    return plt



