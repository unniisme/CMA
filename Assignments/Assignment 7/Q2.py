from ODE import ODE, nODE
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class HeatEquation2D(ODE):
    
    def __init__(self, u_0, g, M, f, mu = 1):
        """
        PDE is for x ∈ (a,b). u(a,t) = u_a, u(b,t) = u_b ∀t > 0.
        u(x,y,0) = g(x,y) ∀x ∈ [a,b]

        Returns u as a function of x at time t

        Discretizes x into M intervals.

        f : (x,y,t) -> R
        """
        self.dx = 1/M
        self.M = M

        self.mu = mu
        self.f = f

        self.u_0 = u_0

        self.t = 0

        X, Y = np.mgrid[0:1:M*1j, 0:1:M*1j]
        self.XY = np.stack((X, Y))
        self.value = np.apply_along_axis(lambda pos: g(*pos), 0, self.XY)
        self.initial_value = self.value.copy()

    def forward_euler(self, dt):
        """
        u(i,j,t+1) = u(i,j,t+1) + (μ*dt/(dx²)) * (u(i+1,j,t) + u(i-1,j,t) + u(i,j+1,t) + u(i,j-1,t) - 4u(i,j,t) + f(x,y,t))
        """
        r =  (self.mu*dt/self.dx**2)
        for i in range(1,self.M-1):
            for j in range(1,self.M-1):
                du = r * (self.value[i+1][j] + self.value[i-1][j] + self.value[i][j+1] + self.value[i][j-1] - 4*self.value[i][j]) + self.f(*self.XY[:,i,j],self.t)
                self.value[i][j] += du

        # Apply boundary conditions along grid boundary
        edgeValues = np.apply_along_axis(lambda pos: self.u_0(*pos, self.t), 0, self.XY)
        self.value[0] = edgeValues[0]
        self.value[-1] = edgeValues[-1]
        self.value[:,0] = edgeValues[:,0]
        self.value[:,-1] = edgeValues[:,-1]

        self.t += dt



def animate(frame, eqn, dt, im):

    [eqn.forward_euler(dt) for i in range(10)]

    val = eqn()
    im.set_data(val)

def VisualizeSheet(xc, yc, M=20):
    eqn = HeatEquation2D(lambda x,y,t:0.0, lambda x,y:0.0, M, lambda x,y,t: np.exp(-np.sqrt((x-xc)**2 + (y-yc)**2)))

    dt = 0.0001

    fig, ax = plt.subplots()
    im = ax.imshow(eqn(), vmin=0, vmax=400)

    ani = animation.FuncAnimation(fig, animate, interval=1, fargs=(eqn,dt,im))

    plt.show()



if __name__ == '__main__':
    
    VisualizeSheet(0.5, 0.3, 25)
