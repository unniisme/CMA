from ODE import ODE, nODE
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class InterpolatedFunction:

    def __init__(self, x_ar, f_ar):
        self.x_ar = x_ar
        self.f_ar = f_ar

    def __setitem__(self, index, item):
        self.f_ar[index] = item

    def __getitem__(self, index):
        return self.f_ar[index]

    def __call__(self, x):
        return np.interp(x, self.x_ar, self.f_ar)

    def copy(self):
        return InterpolatedFunction(self.x_ar.copy(), self.f_ar.copy())


class HeatEquation1D(ODE):
    
    def __init__(self, a, b, u_a, u_b, g, M, mu = 1):
        """
        PDE is for x ∈ (a,b). u(a,t) = u_a, u(b,t) = u_b ∀t > 0.
        u(x,0) = g(x) ∀x ∈ [a,b]

        Returns u as a function of x at time t

        Discretizes x into M intervals.

        f(x,t) is assumed to be 0
        """
        self.a = a
        self.b = b
        self.M = M
        self.dx = (b-a)/M

        self.mu = mu

        self.u_a = u_a
        self.u_b = u_b

        self.approximation_matrix = np.zeros((M, M))
        for i in range(1,M-1):
            self.approximation_matrix[i][i-1] = 1
            self.approximation_matrix[i][i] = -2
            self.approximation_matrix[i][i+1] = 1

        X = np.linspace(a, b, M)
        self.value = InterpolatedFunction(X, np.vectorize(g)(X))
        self.initial_value = self.value.copy()

    def forward_euler(self, dt):
        """
        u(t+1) = u(t) + (μ*dt/(dx²)) Au
        """
        du = (self.mu*dt/self.dx**2) * self.approximation_matrix @ self.value.f_ar
        self.value.f_ar += du

        self.value.f_ar[0] = self.u_a
        self.value.f_ar[-1] = self.u_b

    def backward_euler(self, dt):
        """
        not working sorry :(
        """
        coeff = np.identity(self.M) - (self.mu*dt/self.dx**2) * self.approximation_matrix
        du =  (np.linalg.inv(coeff)) @ self.value.f_ar
        self.value.f_ar += du

        self.value.f_ar[0] = self.u_a
        self.value.f_ar[-1] = self.u_b

    def forward_euler_iterative(self, dt):
        u = self.value.f_ar
        r = (self.mu/(self.dx**2))*dt
        for i in range(1,self.M-1):
            u[i] +=  r * (u[i-1] - 2*u[i] + u[i+1])

        u[0] = self.u_a
        u[-1] = self.u_b
        

    def PlotPiece(self):
        plt.plot(self.value.x_ar, self.value.f_ar)



#Init

eqn = HeatEquation1D(0, 1, 0, 0, lambda x: np.exp(-x), 100)
dt = 0.00001

# Set up the figure and axes
fig, ax = plt.subplots()
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 2)

# Define the animation function
def animate(i):
    ax.clear()
    plt.title(str(i*1000*dt))

    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 2)

    if int(dt*1000) <= 0:
        for i in range(int(0.001/dt)):
            eqn.forward_euler(dt)
    else:
        eqn.forward_euler(dt)
    eqn.PlotPiece()



if __name__ == '__main__':

    # Create the animation object
    ani = animation.FuncAnimation(fig, animate, interval=int(dt*1000) if int(dt*1000)>0 else 1)

    # Display the animation
    plt.show()
        

    