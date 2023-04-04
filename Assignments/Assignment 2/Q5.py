import networkx as nx
import matplotlib.pyplot as plt

class Lattice:
    def __init__(self, n):
        self.G = nx.grid_2d_graph(n, n)
    
    def show(self):
        nx.draw(self.G)
        plt.show()


l = Lattice(10)
l.show()