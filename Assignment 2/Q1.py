import matplotlib.pyplot as plt
import random


class UndirectedGraph:

    def __init__(self, n = None):
        self.n = n

        self.numEdges = 0

        if n == None:
            self.numNodes = 0
            self.adjlist = {}
        else:
            self.numNodes = n
            self.adjlist = {i+1:[] for i in range(self.numNodes)}

    def addNode(self, index):
        if type(index) != int or index <= 0:
            raise Exception("Invalid index")

        if self.n != None:
            if index > self.n:
                raise Exception("Node index cannot exceed number of nodes")
            return

        if index not in self.adjlist.keys(): 
            self.adjlist[index] = []
            self.numNodes += 1

    def addEdge(self, u, v):
        self.addNode(u)
        self.addNode(v)

        if v not in self.adjlist[u]:
            self.adjlist[u].append(v)
            self.adjlist[v].append(u)
            self.numEdges += 1

    def copy(self):
        newGraph = UndirectedGraph(self.n)

        newGraph.adjlist = self.adjlist.copy()
        newGraph.numNodes = self.numNodes
        newGraph.numEdges = self.numEdges

        return newGraph

    def plotDegDist(self):
        degFreq = [0] * self.numNodes
        degs = [len(self.adjlist[node]) for node in self.adjlist]
        for deg in degs:
            degFreq[deg] += 1

        distribution = [d/self.numNodes for d in degFreq]
        average = sum(degs)/len(degs)

        plt.scatter(range(self.numNodes), distribution, label='Actual Degree Distribution')
        plt.axvline(x=average, c='r', label="Avg. Node Degree")
        plt.xlabel('Node Degree')
        plt.ylabel('Fraction of Nodes')
        plt.title("Node Degree distribution")
        plt.legend()
        plt.grid()
        plt.show()


    ## Overloads
    def __add__(self, other):
        if type(other) not in [int, tuple]:
            raise TypeError("Graphs can only be added with int or (int, int)")

        if type(other) == tuple:
            if len(other) != 2:
                raise Exception("Only 2-tuples are allowed")

            newG = self.copy()
            newG.addEdge(*other)
            return newG

        else:
            newG = self.copy()
            newG.addNode(other)
            return newG

        
    def __str__(self):
        string = "Graph with " + str(self.numNodes) + " nodes and " + str(self.numEdges) + " edges. Neighbours of the nodes are as below:\n"
        for node in self.adjlist:
            string += "Node " + str(node) + ": " + str(self.adjlist[node])
            string += "\n"
        return string

if __name__ == '__main__':
    g = UndirectedGraph(5)
    g = g + (1, 2)
    g = g + (3, 4)
    g = g + (1, 4)
    print(g)
