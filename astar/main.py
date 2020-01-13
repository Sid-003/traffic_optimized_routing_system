import random

from matplotlib.artist import Artist
from matplotlib.axes import Axes

from imagegen import generate_image
from astar import astar
from node import Node, Graph
from roads import Road

graph = Graph()
nodes = []
for i in range(5):
    x = random.randint(0, 50)
    y = random.randint(0, 50)
    if not((x, y) in nodes):
        nodes.append((x, y))
        n = Node(i+1, (x, y))
        graph.nodes.append(n)

#print(list(reversed([x.pos for x in astar(graph, Node(1, (0, 0)), Node(5, (2, 2)))])))



plt = generate_image(graph)
ax: Axes = plt.gca()
plt.show()

