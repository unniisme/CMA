## References : 
# https://www.autodesk.com/research/publications/real-time-fluid-dynamics
# https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_equations
# https://hplgit.github.io/INF5620/doc/pub/main_ns.pdf

import numpy as np

lerp = lambda a,b,k: a + k*(b-a)


class NS_sim:

    dt = 0.01
    diff_coeff = 0.1
    visc_coeff = 1

    iterations = 20

    def __init__(self, dimensions : tuple):
        self.dimensions = dimensions
        self.D = np.zeros(dimensions)
        self.V = np.zeros((dimensions[0], dimensions[1], 2))
        self.D_prev = np.zeros(dimensions)
        self.V_prev = np.zeros((dimensions[0], dimensions[1], 2))

        self._params = {"D" : [self.D, self.D_prev], "V" : [self.V, self.V_prev]}

    def diffuse(self, param, const, dt):

        k = const*dt*self.dimensions[0]*self.dimensions[1]

        old_param = self._params[param][0].copy()

        for interation in range(self.iterations):
            for i in range(self.dimensions[0]):
                for j in range(self.dimensions[1]):
                    try:
                        s = (self._params[param][0][i+1,j] + self._params[param][0][i-1,j] + self._params[param][0][i,j+1] + self._params[param][0][i,j-1])
                        self._params[param][0][i,j] = (4*self._params[param][1][i,j] + k * s)/(4+4*k)
                    except:
                        pass

        self._params[param][1] = old_param

    def advect(self, param, dt, iterations = 20):

        old_param = self._params[param][0].copy()

        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                f = np.array([i,j]) - dt*self.V[i,j]
                f = np.clip(f, [0.5,0.5], [self.dimensions[0]-1.5, self.dimensions[1]-1.5])

                fract, floor = np.modf(f)
                floor = np.asarray(floor, int)

                z1 = lerp(self._params[param][0][floor[0], floor[1]], self._params[param][0][floor[0]+1, floor[1]], fract[0])
                z2 = lerp(self._params[param][0][floor[0], floor[1]+1], self._params[param][0][floor[0]+1, floor[1]+1], fract[0])
                self._params[param][0][i,j] = lerp(z1, z2, fract[1])
                
                # x = i - dt*self.V[i,j][0]
                # y = j - dt*self.V[i,j][1]

                # x = max(0.5, min(self.dimensions[0]-1.5, x))
                # y = max(0.5, min(self.dimensions[1]-1.5, y))

                # i0 = int(x)
                # i1 = i0+1
                # j0 = int(y)
                # j1 = j0+1

                # s1 = x-i1
                # s0 = 1-s1
                # t1 = y-j1
                # t0 = 1-t1

                # self._params[param][0][i,j] = s0*(t0*self._params[param][1][i0,j0] + t1*self._params[param][1][i0,j1]) + s1*(t0*self._params[param][1][i1,j0] + t1*self._params[param][1][i1,j1])

        self._params[param][1] = old_param


    def curl(self):

        div = np.zeros(self.dimensions)
        p = np.zeros(self.dimensions)
        for i in range(1,self.dimensions[0]-1):
            for j in range(1, self.dimensions[1]-1):
                div[i,j] = (self.V[i+1, j][0] - self.V[i-1, j][0] + self.V[i, j+1][1] - self.V[i, j-1][1])*0.5

        
        for iteration in range(NS.iterations):
            for i in range(1,self.dimensions[0]-1):
                for j in range(1, self.dimensions[1]-1):    
                    p[i,j] = (p[i-1, j] + p[i+1,j] + p[i, j-1] + p[i, j+1]  -  div[i,j])/4

        k = 0.5*self.dimensions[0] #Keeping it like this for now, in reference to paper
        for i in range(1,self.dimensions[0]-1):
            for j in range(1, self.dimensions[1]-1):
                self.V[i,j][0] -= k*p[i+1,j] - p[i-1, j]
                self.V[i,j][1] -= k*p[i,j+1] - p[i, j+1]


    def update(self, dt):

        # Upadate velocity
        self.diffuse("V", self.visc_coeff, dt)
        self.curl()
        self.advect("V", dt)
        self.curl()


        # Update density
        # self.D_prev, self.D = self.D, self.D_prev
        self.diffuse("D", self.diff_coeff, dt)
        # self.D_prev, self.D = self.D, self.D_prev
        self.advect("D", dt)


class NS:

    dt = 0.01
    diff_coeff = 10
    visc_coeff = 1

    iterations = 20 #Number of iterations for guass-siedel method

    def __init__(self, dimensions : tuple):
        self.dimensions = dimensions
        self.D = np.zeros(dimensions)
        self.V = np.zeros((dimensions[0], dimensions[1], 2))
        self.D_prev = np.zeros(dimensions)
        self.V_prev = np.zeros((dimensions[0], dimensions[1], 2))

    def diffuse(self, x, x0, const, dt):
        k = const*dt*self.dimensions[0]*self.dimensions[1]

        old_param = x.copy() #Handle outside

        for interation in range(NS.iterations):
            for i in range(1,self.dimensions[0]-1):
                for j in range(1,self.dimensions[1]-1):
                    s = (x[i+1,j] + x[i-1,j] + x[i,j+1] + x[i,j-1])
                    x[i,j] = (4*x0[i,j] + k * s)/(4+4*k)

        x0 = old_param  #Handle outside

    def advect(self, x, x0, v, dt):
        dt = dt*(np.sqrt(self.dimensions[0]*self.dimensions[1]))

        # old_x = x.copy() #Handle outside

        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                f = np.array([i,j]) - dt*v[i,j]
                f = np.clip(f, [0.5,0.5], [self.dimensions[0]-1.5, self.dimensions[1]-1.5])

                fract, floor = np.modf(f)
                floor = np.asarray(floor, int)

                z1 = lerp(x[floor[0], floor[1]], x[floor[0]+1, floor[1]], fract[0])
                z2 = lerp(x[floor[0], floor[1]+1], x[floor[0]+1, floor[1]+1], fract[0])
                x[i,j] = lerp(z1, z2, fract[1])
                
                # x = i - dt*v[i,j][0]
                # y = j - dt*v[i,j][1]

                # x = max(0.5, min(self.dimensions[0]-1.5, x))
                # y = max(0.5, min(self.dimensions[1]-1.5, y))

                # i0 = int(x)
                # i1 = i0+1
                # j0 = int(y)
                # j1 = j0+1

                # s1 = x-i1
                # s0 = 1-s1
                # t1 = y-j1
                # t0 = 1-t1

                # self.D[i,j] = s0*(t0*x0[i0,j0] + t1*x0[i0,j1]) + s1*(t0*x0[i1,j0] + t1*x0[i1,j1])

        # x0 = old_x #Handle externally

    def curl(self, v):

        div = np.zeros(self.dimensions)
        p = np.zeros(self.dimensions)
        for i in range(1,self.dimensions[0]-1):
            for j in range(1, self.dimensions[1]-1):
                div[i,j] = (v[i+1, j][0] - v[i-1, j][0] + v[i, j+1][1] - v[i, j-1][1])*0.5

        
        for iteration in range(NS.iterations):
            for i in range(1,self.dimensions[0]-1):
                for j in range(1, self.dimensions[1]-1):    
                    p[i,j] = (p[i-1, j] + p[i+1,j] + p[i, j-1] + p[i, j+1]  -  div[i,j])/4

        k = 0.5*self.dimensions[0] #Keeping it like this for now, in reference to paper
        for i in range(1,self.dimensions[0]-1):
            for j in range(1, self.dimensions[1]-1):
                v[i,j][0] -= k*p[i+1,j] - p[i-1, j]
                v[i,j][1] -= k*p[i,j+1] - p[i, j+1]


    def update(self, dt):

        # Upadate velocity
        self.V_prev, self.V = self.V, self.V_prev
        self.diffuse(self.V, self.V_prev, self.visc_coeff, dt)
        self.curl(self.V)
        self.V_prev, self.V = self.V, self.V_prev
        self.advect(self.V, self.V_prev, self.V, dt)
        self.curl(self.V)


        # Update density
        # self.D_prev, self.D = self.D, self.D_prev
        self.diffuse(self.D, self.D_prev, self.diff_coeff, dt)
        # self.D_prev, self.D = self.D, self.D_prev
        self.advect(self.D, self.D_prev, self.V, dt)