import numpy as np
import matplotlib.pyplot as plt
from Vector import Vector2
from Q3 import ODE, nODE
from matplotlib.animation import FuncAnimation

class GravityBodies(nODE):
    """
    A class to model a group of bodies interacting through gravity.

    aₙ = {sum over i!=n} (G mᵢ) ((rᵢ - rₙ)/||rᵢ - rₙ||³)
    dvₙ/dt = aₙ
    drₙ/dt = vₙ
    """
    G = 6.67e-11

    class Body(ODE):
        def __init__(self, r0 : Vector2, v0 : Vector2, m, radius, bodies):
            """
            Initializes the Body class.

            Args:
            r0: initial position vector of the body
            v0: initial velocity vector of the body
            m: mass of the body
            radius: radius of the body
            bodies: the list of all bodies in the group except for self
            """

            self.m = m
            self.radius = radius
            self.v = v0
            self.r = r0
            self._bodies = bodies

        def __call__(self, variable = 'r'):
            """
            Returns the current value of the specified variable.

            Args:
            variable: which variable to return, 'r' or 'v' (default is 'r')

            Returns:
            The current values of the specified variable.
            """
            if variable in ['v', 'velocity']:
                return self.v
            return self.r

        def forward_euler(self, h):
            def bodyForce(body:GravityBodies.Body) -> Vector2:
                """
                Calculates the gravitational force exerted on the Body by another body.

                Args:
                body: the body exerting force on the Body

                Returns:
                The gravitational force Vector2 exerted on the body by the other body.
                """
                disp = (body.r - self.r)
                # if abs(disp) < self.radius:
                #     return Vector2(0, 0)

                return G*body.m*disp/(abs(disp)**3)

            a = sum([bodyForce(body) for body in self._bodies if self != body], start=Vector2(0,0))

            self.v += a*h
            self.r += self.v*h

    def __init__(self, G = 6.67e-11):
        # Add bodies separately
        self.G = G

        self._ODEs = {}
        self.bodies = []

    
    def AddBody(self, r0 : Vector2, v0 : Vector2, m, radius):
        """
        Adds a new Body to the group of bodies.

        Args:
        r0: initial position vector of the Body
        v0: initial velocity vector of the Body
        m: mass of the Body
        radius: radius of the Body
        """
        body = GravityBodies.Body(r0, v0, m, radius, self.bodies)
        self.bodies.append(body)
        self._ODEs[len(self._ODEs)] = body


def SimulateBodies(bodySystem : GravityBodies, dt):
    n = len(bodySystem.bodies)

    fig, ax = plt.subplots()

    plt.title("Planets!!")
    plt.grid()
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    circles = []

    for i in range(n):
        circle = plt.Circle(bodySystem.bodies[i](), bodySystem.bodies[i].radius, fc='r', zorder=10)
        ax.add_patch(circle)
        circles.append(circle)

    # Set the axis limits

    # Function to update the pendulum's position
    def update(frame):
        bodySystem.forward_update(dt)

        # Calculate bounding
        com = sum([body()*body.m for body in bodySystem.bodies], Vector2(0,0))/sum([body.m for body in bodySystem.bodies])
        span = max(max([body()[0] for body in bodySystem.bodies]), max([body()[1] for body in bodySystem.bodies]))

        ax.set_xlim(((com[0]-span)-1, (com[0]+span)+1))
        ax.set_ylim(((com[1]-span)-1, (com[1]+span)+1))
        ax.set_aspect('equal', adjustable='box')

        for i in range(n):
            circles[i].center = bodySystem.bodies[i]()

        return tuple(circles)

    # Create the animation object
    anim = FuncAnimation(fig, update, interval = dt*1000)

    plt.show()


# def PlotBodies(bodySystem : GravityBodies, dt, t_max):
#     t = 0

#     T = []
#     bodyPoses = {}
#     for body in bodySystem.bodies:
#         bodyPoses [body] = []

#     while t<t_max:
#         bodySystem.forward_update(dt)

#         t += dt
#         T.append(t)


def plot_bodies(gb : GravityBodies, h, total_time):
    """
    Plots the paths of the 3 bodies over time.

    Args:
    r0s: a list of Vector2 objects representing the initial positions of the 3 bodies
    v0s: a list of Vector2 objects representing the initial velocities of the 3 bodies
    total_time: the total time for which to simulate the motion of the 3 bodies
    """

    # Set the timestep size and number of timesteps
    N = int(total_time/h)

    # Initialize lists to store the positions of the 3 bodies over time
    r0_history = []
    r1_history = []
    r2_history = []

    # Simulate the motion of the 3 bodies over time
    for i in range(0, N):
        gb.forward_update(h)
        r0_history.append(tuple(gb.bodies[0]()))
        r1_history.append(tuple(gb.bodies[1]()))
        r2_history.append(tuple(gb.bodies[2]()))

    # Extract the x and y coordinates of the 3 bodies over time
    x0, y0 = zip(*r0_history)
    x1, y1 = zip(*r1_history)
    x2, y2 = zip(*r2_history)

    # Plot the paths of the 3 bodies over time
    plt.plot(x0, y0, '-', label='Body 1')
    plt.plot(x1, y1, '-', label='Body 2')
    plt.plot(x2, y2, '-', label='Body 3')
    plt.legend(loc='best')
    plt.show()

    
if __name__ == '__main__':

    G = 6.67e-11

    dt = 0.001
    t = 100

    bodySystem = GravityBodies()

    bodySystem.AddBody(Vector2(0,0), Vector2(0,0), 0.001/G, 0.1)
    bodySystem.AddBody(Vector2(2,2), Vector2(0,0), 0.001/G, 0.1)
    bodySystem.AddBody(Vector2(3,-4), Vector2(0,0), 0.001/G, 0.1)

    # SimulateBodies(bodySystem, dt)

    plot_bodies(bodySystem,  dt, t)

