from Q1 import UndirectedGraph
from Q2 import ERRandomGraph
import matplotlib.pyplot as plt
import random
import math


def isConnected(graph : UndirectedGraph()):

    frontier = [list(graph.adjlist.keys())[0]]
    expanded = []

    # BFS
    while len(frontier) > 0:
        curr = frontier.pop(0)
        
        frontier += [neigh for neigh in graph.adjlist[curr] if ((neigh not in expanded) and (neigh not in frontier))]

        expanded.append(curr)

    return len(expanded) == len(graph.adjlist)

UndirectedGraph.isConnected = isConnected


if __name__ == '__main__':

    numSamples = 100
    graphSize = 100
    resolution = 100

    P = [i/resolution for i in range(resolution)]
    connectedFraction = []

    for p in P:
        numConnectedSamples = 0
        # print(p)
        for i in range(numSamples):
            g = ERRandomGraph(graphSize)
            g.sample(p)
            if g.isConnected():
                numConnectedSamples += 1

        connectedFraction.append(numConnectedSamples/numSamples)
            

    plt.plot(P, connectedFraction)
    plt.axvline(x=math.log(graphSize)/graphSize, c='r', label="Avg. Node Degree")
    plt.show()
    
    plt.plot(P[:int(resolution*0.2)], connectedFraction[:int(resolution*0.2)])
    plt.axvline(x=math.log(graphSize)/graphSize, c='r', label="Avg. Node Degree")
    plt.show()
