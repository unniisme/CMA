from NavierStokes import Simulation, WaterSimulation
import numpy as np
import sys
import time

class Simulator:

    def __init__ (self, N = 20, resolution=0, force = 5, source = 1000, diff = 0.0, visc = 0.0, isWaterSim=False):
        self.fps = 60
        self.running = True

        #resolution is dummy

        self.force = force
        self.source = source

        self.dimensions = (N, N)

        if isWaterSim:
            self.fluid = WaterSimulation(N-2, diff, visc, 0, 0.1)
        else:
            self.fluid = Simulation(N-2, diff, visc, 0, 0.1)

    def addSources(self):
        pass
        #Define outside

    def density_color(self, i,j):
        col = round(self.fluid.get_density()[i,j]*255/10)
        col = max(0, min(255,col))
        return (col, col, col)

    def DrawSquare(self, col):
        col = col[0]
        gray = 232+(col//11)
        print("\033[48;5;" + str(gray) + "m  \033[0m", end="")

    def DrawGrid(self, in_offset : int = 0):

        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                self.DrawSquare(self.density_color(i,j))
            print()

    def Start(self):

        print("-------------Running-----------------")

        while True:

            self.fluid.solver.density_prev = np.zeros(self.fluid.solver.dimensions)
            self.fluid.solver.u_prev = np.zeros(self.fluid.solver.dimensions)
            self.fluid.solver.v_prev = np.zeros(self.fluid.solver.dimensions)

            self.addSources()


            self.fluid.update()

            self.DrawGrid()

            print("\033[F"*(self.fluid.solver.N+3))

            time.sleep(1/self.fps)

angle = 0
def addSources(sim : Simulator):
    N = sim.fluid.solver.N
    sim.fluid.add_density(N//2, N//2, sim.source)

    global angle
    force = (np.cos(angle)*sim.force, np.sin(angle)*sim.force)
    angle+=0.01
    sim.fluid.add_velocity(N//2, N//2, *force)

def set_bnd(self, b, x):
    x[0,:] = np.where(b==1, -x[1,:], x[1,:])
    x[self.N+1,:] = np.where(b==1, -x[self.N,:], x[self.N,:])
    x[:,0] = 0
    x[:,self.N+1] = np.where(b==2, -x[:,self.N], x[:,self.N])

    # Make the bottom sticky to prevent leakage
    x[:,self.N+1] = np.where(b == 0, 0, -x[:,self.N])

    x[0,0] = 0.5*(x[1,0]+x[0,1])
    x[0,self.N+1] = 0.5*(x[1,self.N+1]+x[0,self.N])
    x[self.N+1,0] = 0.5*(x[self.N,0]+x[self.N+1,1])
    x[self.N+1,self.N+1] = 0.5*(x[self.N,self.N+1]+x[self.N+1,self.N])

if __name__ == '__main__':

    print("N = 32, force = 70, source = 700, diff = 0.0, visc = 0.0")
    sim = Simulator(N=32, force = 70, source=700, diff = 0.0, visc = 0.0)

    sim.addSources = lambda :addSources(sim)
    sim.fluid.solver.set_bnd = lambda b,x: set_bnd(sim.fluid.solver, b, x)

    sim.Start()