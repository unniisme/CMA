from Q1 import UndirectedGraph
from Q2 import ERRandomGraph
import matplotlib.pyplot as plt

def oneTwoCompomentSizes(graph : UndirectedGraph()):

    componentSizes = [] 

    nodes = list(graph.adjlist.keys())

    frontier = [nodes.pop()]
    expanded = []
    componentSize = 0

    # BFS
    while len(frontier) > 0:
        curr = frontier.pop(0) 
        componentSize += 1
        
        frontier += [neigh for neigh in graph.adjlist[curr] if ((neigh not in expanded) and (neigh not in frontier))]

        expanded.append(curr)
        try:
            nodes.remove(curr)
        except:
            pass

        if len(frontier) == 0 and len(nodes) > 0:
            componentSizes.append(componentSize)
            componentSize = 0
            frontier = [nodes.pop()]

    if len(componentSizes) == 0:
        return [componentSize, 0]

    return sorted(componentSizes+[componentSize], reverse=True)[:2]
    
UndirectedGraph.oneTwoCompomentSizes = oneTwoCompomentSizes

if __name__ == '__main__':
    g = UndirectedGraph()
    g = g + (1, 2)
    g = g + (3, 4)
    g = g + (6, 4)
    print(g.oneTwoCompomentSizes())

    g = ERRandomGraph(100)
    g.sample(0.01)
    print(g.oneTwoCompomentSizes())

    n = 1000

    P = [i/100000 for i in range(int(1000))]
    firstFractions = []
    secondFractions = []
    for p in P:
        g = ERRandomGraph(n)
        g.sample(p)
        first, second = g.oneTwoCompomentSizes()
        firstFractions.append(first/n)
        secondFractions.append(second/n)

    plt.plot(P, firstFractions, label="Largest connected component")
    plt.plot(P, secondFractions, label="Second largest connected component")
    plt.xlabel('p')
    plt.ylabel('fraction of nodes')
    plt.title("Fraction of largest and second largest components")
    plt.legend()
    plt.grid()
    plt.show()

        
