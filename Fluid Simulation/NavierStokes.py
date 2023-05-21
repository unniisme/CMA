import numpy as np


class FluidSolver:
    def __init__(self, N, diff, visc, dt):
        self.N = N
        self.dt = dt
        self.diff = diff
        self.visc = visc

        # allocate memory for velocity and density fields
        self.dimensions = (N+2, N+2)
        size = (N+2)*(N+2)
        self.size = size
        self.u = np.zeros(self.dimensions)
        self.v = np.zeros(self.dimensions)
        self.u_prev = np.zeros(self.dimensions)
        self.v_prev = np.zeros(self.dimensions)
        self.density = np.zeros(self.dimensions)
        self.density_prev = np.zeros(self.dimensions)

    def add_source(self, x, s):
        x += self.dt*s

    def set_bnd(self, b, x):
        x[0,:] = np.where(b==1, -x[1,:], x[1,:])
        x[self.N+1,:] = np.where(b==1, -x[self.N,:], x[self.N,:])
        x[:,0] = np.where(b==2, -x[:,1], x[:,1])
        x[:,self.N+1] = np.where(b==2, -x[:,self.N], x[:,self.N])

        x[0,0] = 0.5*(x[1,0]+x[0,1])
        x[0,self.N+1] = 0.5*(x[1,self.N+1]+x[0,self.N])
        x[self.N+1,0] = 0.5*(x[self.N,0]+x[self.N+1,1])
        x[self.N+1,self.N+1] = 0.5*(x[self.N,self.N+1]+x[self.N+1,self.N])


    def lin_solve(self, b, x, x0, a, c):
        for k in range(20):
            x[1:-1, 1:-1] = (x0[1:-1, 1:-1] + a*(x[:-2, 1:-1] + x[2:, 1:-1] + x[1:-1, :-2] + x[1:-1, 2:])) / c
            self.set_bnd(b, x)

    def diffuse(self, b, x, x0, diff):
        a = self.dt*diff*self.N*self.N
        self.lin_solve(b, x, x0, a, 1+4*a)

    def advect(self, b, d, d0, u, v):
        dt0 = self.dt*self.N
        for i in range(1, self.N+1):
            for j in range(1, self.N+1):
                x = i-dt0*u[(i,j)]
                y = j-dt0*v[(i,j)]
                if x < 0.5:
                    x = 0.5
                if x > self.N+0.5:
                    x = self.N+0.5
                i0 = int(x)
                i1 = i0+1
                if y < 0.5:
                    y = 0.5
                if y > self.N+0.5:
                    y = self.N+0.5
                j0 = int(y)
                j1 = j0+1
                s1 = x-i0
                s0 = 1-s1
                t1 = y-j0
                t0 = 1-t1
                d[(i,j)] = s0*(t0*d0[(i0,j0)]+t1*d0[(i0,j1)])+s1*(t0*d0[(i1,j0)]+t1*d0[(i1,j1)])
        self.set_bnd(b, d)


    def project(self):
        self.divergence()
        self.pressure = np.zeros(self.dimensions)

        self.lin_solve(0, self.pressure, self.div, 1, 4)

        for i in range(1, self.N+1):
            for j in range(1, self.N+1):
                self.u[(i,j)] -= 0.5*self.N*(self.pressure[(i+1,j)]-self.pressure[(i-1,j)])
                self.v[(i,j)] -= 0.5*self.N*(self.pressure[(i,j+1)]-self.pressure[(i,j-1)])

        self.set_bnd(1, self.u)
        self.set_bnd(2, self.v)

    def divergence(self):
        self.div = np.zeros(self.dimensions)
        for i in range(1, self.N+1):
            for j in range(1, self.N+1):
                self.div[(i,j)] = -0.5*(self.u[(i+1,j)]-self.u[(i-1,j)]+self.v[(i,j+1)]-self.v[(i,j-1)])/self.N

        self.set_bnd(0, self.div)

    def vel_step(self):
        self.add_source(self.u, self.u_prev)
        self.add_source(self.v, self.v_prev)

        self.u_prev, self.u = self.u, self.u_prev
        self.v_prev, self.v = self.v, self.v_prev

        self.diffuse(1, self.u, self.u_prev, self.visc)
        self.diffuse(2, self.v, self.v_prev, self.visc)

        self.project()

        self.u_prev, self.u = self.u, self.u_prev
        self.v_prev, self.v = self.v, self.v_prev

        self.advect(1, self.u, self.u_prev, self.u_prev, self.v_prev)
        self.advect(2, self.v, self.v_prev, self.u_prev, self.v_prev)

        self.project()

    def dens_step(self):
        self.add_source(self.density, self.density_prev)

        self.density_prev, self.density = self.density, self.density_prev

        self.diffuse(0, self.density, self.density_prev, self.diff)

        self.density_prev, self.density = self.density, self.density_prev

        self.advect(0,self.density, self.density_prev, self.u, self.v)

class SmokeSimulation:
    def __init__(self, N, diff, visc, dt):
        self.solver = FluidSolver(N, diff, visc, dt)

    def add_density(self, x, y, amount):
        self.solver.density_prev[(int(x), int(y))] += amount

    def add_velocity(self, x, y, amountX, amountY):
        self.solver.u_prev[(int(x), int(y))] += amountX
        self.solver.v_prev[(int(x), int(y))] += amountY

    def update(self):
        self.solver.vel_step()
        self.solver.dens_step()

    def get_density(self):
        return self.solver.density

# To use this code, you can create a `SmokeSimulation` object with the desired parameters (grid size, diffusion, viscosity, time step). Then, you can call the `add_density` and `add_velocity` methods to add sources of smoke and wind to the simulation. Finally, you can call the `update` method to advance the simulation by one time step. Here's an example:
if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # create smoke simulation with 64x64 grid, diffusion=0.01, viscosity=0.1, dt=0.1
    sim = SmokeSimulation(64, 0.01, 0.1, 0.1)

    # add some smoke and wind sources
    sim.add_density(0.5, 0.5, 100)
    sim.add_velocity(0.5, 0.5, 2, 0)

    # run simulation for 100 time steps
    for i in range(100):
        print (i)
        sim.update()

    # display density field as grayscale image
    plt.imshow(np.array(sim.solver.density).reshape(sim.solver.N+2, sim.solver.N+2), cmap='gray')
    plt.show()
