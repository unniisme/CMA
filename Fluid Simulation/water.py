from simulator import Simulator
import sys
import numpy as np

restitution = 2

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

def ext(fluid):
    fluid.apply_gravity()
    fluid.add_density(fluid.solver.N/2, fluid.solver.N/4, 1000)

def density_color(sim, i, j):
    col = round(sim.fluid.get_density()[i,j]*255/10)
    col = max(0, min(255,col))
    v_x, v_y = sim.fluid.get_velocity(i,j)
    mod = abs(v_x + v_y)
    col1 = int(min(255, col*(mod/2)))
    return (col1, col1, col)


if __name__ == '__main__':

    print("N = 64, resolution = 10, force = 70, source = 1000, diff = 0.0, visc = 0.0, temp_diff = 0.0")
    sim = Simulator(N=64, resolution=10, force = 70, source=1000, diff = 0.0, visc = 0.0, temp_diff = 0.0, isWaterSim=True)

    sim.fluid.ext_update = lambda : ext(sim.fluid)
    sim.density_color = lambda i,j: density_color(sim, i, j)
    sim.fluid.solver.set_bnd = lambda b,x: set_bnd(sim.fluid.solver, b, x)
    sim.Start()

    