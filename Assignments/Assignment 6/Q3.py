import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class ODE:
    """
    Represents a single ODE. Includes initial value, euler method function definition and is updatable.
    Abstract class.

    forward_euler : Updation function using forward Euler method.
    backward_euler : Updation function using backward Euler method.
    Both takes input the class and the value of h
    ie. forward_euler(self, h) updates the value of x and t in the current step of the ODE.
    """

    def __init__(self, initial_value):
        # Abstraction
        self.initial_value = initial_value
        self.value = initial_value

    def __call__(self):
        return self.value

    def reset(self):
        self.value = self.initial_value

class nODE:
    """
    Represents an n-order ODE. Saved as n single order ODEs.
    Abstract class.
    
    _ODEs = {variable name : ODE}
    """

    def __init__(self, **kwargs):
        # This may need to be rephrased to allow interdependant equations
        self._ODEs = kwargs

    def forward_update(self, h):
        for ode in self._ODEs.values():
            ode.forward_euler(h)

    def backward_update(self, h):
        for ode in self._ODEs.values():
            ode.backward_euler(h)

    def get_variable(self, var):
        return self._ODEs[var]()
    
    def reset(self):
        for ode in self._ODEs.values():
            ode.reset()

    def Plot(self, t_final, h, plot_params):
        """
        Function to plot ODEs. plot_params is a list of tuples of (x,y) where x and y are the names of the variables which are to be plotted against each other.
        (x,y, label) can be used to label a plot.
        """
        t = 0
        T = [t]
        vals = {x: [self.get_variable(x)] for x in self._ODEs}

        while t<t_final:
            self.forward_update(h)

            t += h
            T.append(t)

            for x in vals:
                vals[x].append(self.get_variable(x))

        vals['t'] = T
        
        for plot_param in plot_params:
            try:
                x,y, label = plot_param
                plt.plot(vals[x], vals[y], label=label)
            except ValueError as e:
                x,y = plot_param
                plt.plot(vals[x], vals[y])

        # Reset values to initial values after plotting.
        self.reset()


class Pendulum(nODE):
    """
    dω/dt = - μω - (g/L) sin θ(t)
    dθ/dt = ω

    Note this is the equation with friction included as well. μ = 0 will remove friction.
    """
        
    class omegaODE(ODE):
        """Defines the ODE for the angular velocity."""
        def __init__(self, initial_value, theta : ODE, g, L, mu):
            self.theta = theta
            self.g = g
            self.L = L
            self.mu = mu
            super().__init__(initial_value)

        def forward_euler(self, h):
            self.value += (-self.value*self.mu) + (-self.g/self.L)* np.sin(self.theta())*h

    def theta_forward_euler(thetaode, h):
        thetaode.value += thetaode.omega()*h

    # class thetaODE(ODE) can just use abstract class definition

    def __init__(self, omega0, theta0, g, L, mu=0):
        """
        Initializes the Pendulum class with initial angular velocity, initial angle, gravitational constant,
        length of the pendulum, and coefficient of friction.
        """

        theta = ODE(theta0)
        omega = Pendulum.omegaODE(omega0, theta, g, L, mu)

        # class definition for theta ODE
        theta.omega = omega
        theta.forward_euler = lambda h:Pendulum.theta_forward_euler(theta, h)

        super().__init__(theta=theta, omega=omega)


def SimulatePendulum(pendulum : Pendulum, dt):
    fig, ax = plt.subplots()

    plt.title("Simulation of pendulum")

    # Define the line segment and circle for the pendulum
    line, = ax.plot([], [], 'b-', lw=2)
    circle = plt.Circle((0, 0), 0.05, fc='r', zorder=10)
    ax.add_patch(circle)

    # Set the axis limits
    ax.set_xlim((-1.1, 1.1))
    ax.set_ylim((-1.1, 1.1))
    ax.set_aspect('equal', adjustable='box')

    # Function to update the pendulum's position
    def update(frame):
        pendulum.forward_update(dt)

        # Update the position of the line segment and circle
        line.set_data([0, np.sin(pendulum.get_variable("theta"))], [0, -np.cos(pendulum.get_variable("theta"))])
        circle.center = (np.sin(pendulum.get_variable("theta")), -np.cos(pendulum.get_variable("theta")))

        return line, circle,

    # Create the animation object
    anim = FuncAnimation(fig, update, interval = dt*1000)

    plt.show()


if __name__ == '__main__':


    # Simulation parameters
    omega0 = 0 #rad/s
    theta0 = np.pi/2 #rad
    g = 10 #m/s²
    L = 1 #m
    mu = 0 #1/s  ## Change to add damping, it's really fun!!
    pendulum = Pendulum(omega0, theta0, g, L, mu)

    dt = 0.01
    t = 0
    duration = 50

    pendulum.Plot(duration, dt, [('t', 'theta', 'θ (Rad)'), ('t', 'omega', 'ω (Rad/s')])

    plt.title("θ, ω vs time")
    plt.legend()
    plt.xlabel("s")
    plt.ylabel("Angular variables")
    plt.show()

    pendulum.Plot(duration, dt, [('theta', 'omega')])

    plt.title("θ vs ω")
    plt.xlabel("θ")
    plt.ylabel("ω")
    plt.show()

    SimulatePendulum(pendulum, dt)






