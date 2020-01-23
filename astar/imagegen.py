import io
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure

from node import Graph
from roads import Road


# Calculate the transformation shift for the text based on the slope of the edge.
def calculate_shift(dx, dy):
    tf = (0, 0)
    o = 'l'
    s = 0.08
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


# Take two images from memory buffer, composite them, and save to a file.
def composite_and_save(ms1, ms2):
    ms1.seek(0)
    ms2.seek(0)

    img1 = Image.open(ms1)
    img2 = Image.open(ms2)

    total_height = img1.height + img2.height
    output = Image.new('RGBA', (img1.width, total_height))

    output.paste(img1, (0, 0))
    output.paste(img2, (0, img2.height))

    output.save('bruh.png')


# Generate the plot and return the image as a memory buffer.
def generate_image(g: Graph, type, label=True, best_path=[]):
    # Setup Axes for the figure.
    plt.clf()
    cf: Figure = plt.gcf()
    cf.set_size_inches(17, 10)
    ax = cf.add_axes((0, 0, 1, 1))
    if label:
        cf.suptitle("ASTAR" if type == 'astar' else "BNA", fontsize=50, x=0.9, fontdict={'fontname': 'Comic Sans MS'})
    ax.set_facecolor((1, 1, 1))
    nodes = g.nodes
    edges = g.edges.keys()

    # Draw node circles and label the nodes.
    xy = np.asarray([x.pos for x in nodes])
    ax.scatter(xy[:, 0], xy[:, 1], s=1500, c='black', edgecolors=['red'], linewidths=3)
    for node in nodes:
        (x, y) = node.pos
        ax.text(x, y, str(node.id), size=30, fontdict={'fontname': 'Comic Sans MS'}, color='white',
                horizontalalignment='center', verticalalignment='center')

    best_edges = []
    normal_edges = []

    # For each edge, check if the edge needs highlighting and labeling.
    for e in edges:
        p1 = nodes[e[0]].pos
        p2 = nodes[e[1]].pos

        if label:
            label_text(ax, g, e)

        # Add to different collections based on the best path.
        if p1 in best_path and p2 in best_path:
            best_edges.append((p1, p2))
        else:
            normal_edges.append((p1, p2))

    # Create a line collection of the normal edges.
    ne = np.asarray(normal_edges)
    edge_collection = LineCollection(ne, colors='black')
    edge_collection.set_zorder(-50)

    # Create a line collection of the highlighted edges.
    be = np.asarray(best_edges)
    best_path_edge_collection = LineCollection(be, colors='green')
    best_path_edge_collection.set_zorder(-50)

    # Add the collection to the axes for the library to render.
    ax.add_collection(edge_collection)
    ax.add_collection(best_path_edge_collection)
    return save(plt)


# Label the text for each edge based on the load.
def label_text(ax, g, e):
    # Initialize position variable and calculate transformation shift.
    p1 = g.nodes[e[0]].pos
    p2 = g.nodes[e[1]].pos
    (x1, y1) = p1
    (x2, y2) = p2
    dx = x2 - x1
    dy = y2 - y1
    t = calculate_shift(dx, dy)
    tf = t[1]

    # Check the type of load and the direction of the load.
    roadf = g.edges[((g.nodes[e[0]]).id, g.nodes[e[1]].id)]
    roado = g.edges[((g.nodes[e[1]]).id, g.nodes[e[0]].id)]

    load1 = roadf.aload if type == 'astar' else roadf.bload
    load2 = roado.aload if type == 'astar' else roadf.bload

    if t[0] == 'r':
        label = str(round(load1, 2)) + '--->'
    else:
        label = '<---' + str(round(load2, 2))

    # Shift the actual position of the text.
    (x, y) = ((0.5 * (x1 + x2)) + tf[0], (0.5 * (y1 + y2)) + tf[1])

    # Rotate the text to match the slope of the edge.
    angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
    if angle > 90:
        angle -= 180
    if angle < - 90:
        angle += 180

    # Create an array of the position to transform based on the angle.
    xy = np.array((x, y))
    trans_angle = ax.transData.transform_angles(np.array((angle,)),
                                                xy.reshape((1, 2)))[0]

    # Label the text.
    ax.text(x, y, label, size=25, color='red', fontdict={'fontname': 'Comic Sans MS'}, horizontalalignment='center',
            verticalalignment='center',
            rotation=trans_angle,
            zorder=5)


# Create a memory stream to save the file and return it.
def save(plt):
    img = io.BytesIO()
    plt.savefig(img, format='png')
    return img
