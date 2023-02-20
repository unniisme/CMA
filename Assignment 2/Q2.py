from Q1 import UndirectedGraph
import random

class ERRandomGraph(UndirectedGraph):

    def sample(self, p):
        if self.n == None:
            raise Exception("Number of nodes have to be pre-defined")

        if not (0<=p<=1):
            raise Exception("Invalid probability")

        for i in range(self.n):
            for j in range(i+1, self.n):
                toss = random.random()
                if p>=toss:
                    self.addEdge(i+1, j+1)

if __name__ == '__main__':
    g = ERRandomGraph(1000)
    g.sample(0.4)
    g.plotDegDist()  