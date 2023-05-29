# https://www.dgp.toronto.edu/public_user/stam/reality/Research/pdf/GDC03.pdf

import numpy as np


class FluidSolver:
    def __init__(self, N, diff, visc, dt):
        """
        Initialize FluidSolver class with given parameters
        
        Parameters:
        N (int): size of grid
        diff (float): diffusion rate
        visc (float): viscosity rate
        dt (float): time-step size
        """
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

    # May be redefined outside
    def set_bnd(self, b, x):
        """
        Set boundary condition for grid
        
        Parameters:
        b (int): boundary type {0 : d, 1 : u, 2 : v}
        x (ndarray): grid to set boundary condition for
        
        Returns:
        None
        """
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
        """
        Diffuse density in the system according to the given diffusion rate
        
        Parameters:
        b (int): boundary condition type
        x (ndarray): current grid state
        x0 (ndarray): previous grid state
        diff (float): diffusion rate of the density
        """
        a = self.dt*diff*self.N*self.N
        self.lin_solve(b, x, x0, a, 1+4*a)

    def advect(self, b, d, d0, u, v):
        """
        Advects the density field according to the velocity of the fluid
        
        Parameters:
        b (int): boundary condition type
        d (ndarray): current density
        d0 (ndarray): previous density
        u (ndarray): x-velocity field
        v (ndarray): y-velocity field
        """
        dt0 = self.dt * self.N

        # Generate 2D arrays of x and y coordinates
        y, x = np.meshgrid(np.arange(1, self.N+1), np.arange(1, self.N+1))
        x = x.astype(float)
        y = y.astype(float)

        # Calculate the x and y coordinates after advection
        x -= dt0 * u[1:self.N+1, 1:self.N+1]  # u and v have an offset of 1
        y -= dt0 * v[1:self.N+1, 1:self.N+1]

        # Clip x and y to reflect B.C. of the domain
        x = np.clip(x, 0.5, self.N + 0.5)
        y = np.clip(y, 0.5, self.N + 0.5)

        # Get the indices and weights for bilinear interpolation
        i0, j0 = np.floor(x).astype(int), np.floor(y).astype(int)
        i1, j1 = i0 + 1, j0 + 1
        s1, t1 = x - i0, y - j0
        s0, t0 = 1. - s1, 1. - t1

        # Apply bilinear interpolation to advect the density field
        d[1:self.N+1, 1:self.N+1] = s0*(t0*d0[i0, j0] + t1*d0[i0, j1]) + \
                                    s1*(t0*d0[i1, j0] + t1*d0[i1, j1])

        self.set_bnd(b, d)


    def project(self):
        """
        Make velocity field divergence free using helmholtz decomposition
        """
        self.divergence()
        self.pressure = np.zeros(self.dimensions)

        self.lin_solve(0, self.pressure, self.div, 1, 4)

        self.u[1:-1, 1:-1] -= 0.5*self.N*(self.pressure[2:, 1:-1] - self.pressure[:-2, 1:-1])
        self.v[1:-1, 1:-1] -= 0.5*self.N*(self.pressure[1:-1, 2:] -  self.pressure[1:-1, :-2])

        self.set_bnd(1, self.u)
        self.set_bnd(2, self.v)

    def divergence(self):
        """
        Calculates the divergence of the velocity field
        """
        self.div = np.zeros(self.dimensions)
        self.div[1:-1, 1:-1] = -0.5 * (self.u[2:, 1:-1] - self.u[:-2, 1:-1] +
                               self.v[1:-1, 2:] - self.v[1:-1, :-2]) / self.N


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

class Simulation:
    def __init__(self, N, diff, visc, dt):
        self.solver = FluidSolver(N, diff, visc, dt)

    def add_density(self, x, y, amount):
        self.solver.density_prev[(int(x), int(y))] += amount

    def add_velocity(self, x, y, amountX, amountY):
        self.solver.u_prev[(int(x), int(y))] += amountX
        self.solver.v_prev[(int(x), int(y))] += amountY

    def ext_update(self):
        #called every frame. Modify externally to add properties
        pass

    def update(self):
        self.ext_update()
        self.solver.vel_step()
        self.solver.dens_step()

    def get_density(self):
        return self.solver.density

    def get_velocity(self, i, j):
        return (self.solver.u[i,j], self.solver.v[i,j])


class WaterSimulation(Simulation):

    def set_bnd(self, b, x):
        x[0,:] = np.where(b==1, -x[1,:], x[1,:])
        x[self.N+1,:] = np.where(b==1, -x[self.N,:], x[self.N,:])
        x[:,0] *= 0 #Empty top
        x[:,self.N+1] = np.where(b==2, -x[:,self.N], x[:,self.N])

        x[0,0] = 0.5*(x[1,0]+x[0,1])
        x[0,self.N+1] = 0.5*(x[1,self.N+1]+x[0,self.N])
        x[self.N+1,0] = 0.5*(x[self.N,0]+x[self.N+1,1])
        x[self.N+1,self.N+1] = 0.5*(x[self.N,self.N+1]+x[self.N+1,self.N])

    g = 2

    def __init__(self, N, diff, visc, dt):
        self.solver = FluidSolver(N, diff, visc, dt)
        self.solver.set_bnd = lambda b,x: WaterSimulation.set_bnd(self.solver, b, x)

    def apply_gravity(self):
        self.solver.v_prev += WaterSimulation.g*self.solver.dt

    def ext_update(self):
        self.apply_gravity()
