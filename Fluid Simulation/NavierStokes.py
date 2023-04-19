import numpy as np


class FluidSolver:
    def __init__(self, N, diff, visc, dt):
        self.N = N
        self.dt = dt
        self.diff = diff
        self.visc = visc

        # allocate memory for velocity and density fields
        size = (N+2)*(N+2)
        self.size = size
        self.u = [0.0]*size
        self.v = [0.0]*size
        self.u_prev = [0.0]*size
        self.v_prev = [0.0]*size
        self.density = [0.0]*size
        self.density_prev = [0.0]*size

    def add_source(self, s):
        for i in range((self.N+2)*(self.N+2)):
            self.density[i] += self.dt*s[i]

    def set_bnd(self, b, x):
        for i in range(1, self.N+1):
            x[self.IX(0,i)] = -x[self.IX(1,i)] if b == 1 else x[self.IX(1,i)]
            x[self.IX(self.N+1,i)] = -x[self.IX(self.N,i)] if b == 1 else x[self.IX(self.N,i)]
            x[self.IX(i,0)] = -x[self.IX(i,1)] if b == 2 else x[self.IX(i,1)]
            x[self.IX(i,self.N+1)] = -x[self.IX(i,self.N)] if b == 2 else x[self.IX(i,self.N)]

        x[self.IX(0,0)] = 0.5*(x[self.IX(1,0)]+x[self.IX(0,1)])
        x[self.IX(0,self.N+1)] = 0.5*(x[self.IX(1,self.N+1)]+x[self.IX(0,self.N)])
        x[self.IX(self.N+1,0)] = 0.5*(x[self.IX(self.N,0)]+x[self.IX(self.N+1,1)])
        x[self.IX(self.N+1,self.N+1)] = 0.5*(x[self.IX(self.N,self.N+1)]+x[self.IX(self.N+1,self.N)])

    def IX(self, i, j):
        return i + (self.N+2)*j

    def lin_solve(self, b, x, x0, a, c):
        for k in range(20):
            for i in range(1, self.N+1):
                for j in range(1, self.N+1):
                    x[self.IX(i,j)] = (x0[self.IX(i,j)] + a*(x[self.IX(i-1,j)]+x[self.IX(i+1,j)]+x[self.IX(i,j-1)]+x[self.IX(i,j+1)]))/c
            self.set_bnd(b, x)

    def diffuse(self, x, x0, diff):
        a = self.dt*diff*self.N*self.N
        self.lin_solve(0, x, x0, a, 1+4*a)

    def advect(self, d, d0, u, v):
        dt0 = self.dt*self.N
        for i in range(1, self.N+1):
            for j in range(1, self.N+1):
                x = i-dt0*u[self.IX(i,j)]
                y = j-dt0*v[self.IX(i,j)]
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
                d[self.IX(i,j)] = s0*(t0*d0[self.IX(i0,j0)]+t1*d0[self.IX(i0,j1)])+s1*(t0*d0[self.IX(i1,j0)]+t1*d0[self.IX(i1,j1)])
        self.set_bnd(0, d)

    def project(self):
        for i in range(1, self.N+1):
            for j in range(1, self.N+1):
                self.u_prev[self.IX(i,j)] = self.u[self.IX(i,j)]
                self.v_prev[self.IX(i,j)] = self.v[self.IX(i,j)]
                self.density_prev[self.IX(i,j)] = self.density[self.IX(i,j)]

        self.divergence()
        self.pressure = [0.0]*self.size

        self.lin_solve(0, self.pressure, self.div, 1, 4)

        for i in range(1, self.N+1):
            for j in range(1, self.N+1):
                self.u[self.IX(i,j)] -= 0.5*self.N*(self.pressure[self.IX(i+1,j)]-self.pressure[self.IX(i-1,j)])
                self.v[self.IX(i,j)] -= 0.5*self.N*(self.pressure[self.IX(i,j+1)]-self.pressure[self.IX(i,j-1)])

        self.set_bnd(1, self.u)
        self.set_bnd(2, self.v)

    def divergence(self):
        self.div = [0.0]*self.size
        for i in range(1, self.N+1):
            for j in range(1, self.N+1):
                self.div[self.IX(i,j)] = -0.5*(self.u[self.IX(i+1,j)]-self.u[self.IX(i-1,j)]+self.v[self.IX(i,j+1)]-self.v[self.IX(i,j-1)])/self.N

        self.set_bnd(0, self.div)

    def vel_step(self):
        self.add_source(self.u_prev)
        self.add_source(self.v_prev)

        self.diffuse(self.u, self.u_prev, self.visc)
        self.diffuse(self.v, self.v_prev, self.visc)

        self.project()

        for i in range(1, self.N+1):
            for j in range(1, self.N+1):
                self.u_prev[self.IX(i,j)] = self.u[self.IX(i,j)]
                self.v_prev[self.IX(i,j)] = self.v[self.IX(i,j)]

        self.advect(self.u, self.u_prev, self.u_prev, self.v_prev)
        self.advect(self.v, self.v_prev, self.u_prev, self.v_prev)

        self.project()

    def dens_step(self):
        self.add_source(self.density_prev)

        self.diffuse(self.density, self.density_prev, self.diff)
        self.advect(self.density_prev, self.density, self.u, self.v)

class SmokeSimulation:
    def __init__(self, N, diff, visc, dt):
        self.solver = FluidSolver(N, diff, visc, dt)

    def add_density(self, x, y, amount):
        size = 1
        self.solver.density[self.solver.IX(int(x*size), int(y*size))] += amount

    def add_velocity(self, x, y, amountX, amountY):
        size = 1
        self.solver.u[self.solver.IX(int(x*size), int(y*size))] += amountX
        self.solver.v[self.solver.IX(int(x*size), int(y*size))] += amountY

    def update(self):
        self.solver.vel_step()
        self.solver.dens_step()

    def get_density(self):
        N = self.solver.N
        density = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                density[i,j] = self.solver.density[self.solver.IX(i,j)]
        return density

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
