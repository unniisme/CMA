import numpy as np
import matplotlib.pyplot as plt
from Vector import Vector2
from Q3 import ODE, nODE
from matplotlib.animation import FuncAnimation

G = 6.67e-11


class GravityBodies(nODE):
    """
    A class to model a group of bodies interacting through gravity.

    aₙ = {sum over i!=n} (G mᵢ) ((rᵢ - rₙ)/||rᵢ - rₙ||³)
    dvₙ/dt = aₙ
    drₙ/dt = vₙ
    """
    G = 6.67e-11

    class Body(ODE):
        def __init__(self, r0 : Vector2, v0 : Vector2, m, radius, G, bodies):
            """
            Initializes the Body class.

            Args:
            r0: initial position vector of the body
            v0: initial velocity vector of the body
            m: mass of the body
            radius: radius of the body
            bodies: the list of all bodies in the group
            """

            self.m = m
            self.radius = radius
            self.v = v0
            self.r = r0
            self._bodies = bodies
            self.G = G

            self.initial_v = v0
            self.initial_r = r0

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

        def reset(self):
            self.v = self.initial_v.copy()
            self.r = self.initial_r.copy()

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
                dist = abs(disp)

                outForce = self.G*body.m*disp/(dist**3)
                
                #Contact force
                if dist < self.radius + body.radius:
                    outForce -= 10000 * float(np.sqrt(dist)) * disp

                return outForce

            a = sum([bodyForce(body) for body in self._bodies if self != body], start=Vector2(0,0))

            self.v += a*h
            self.r += self.v*h

    def __init__(self, G = 6.67e-11):
        # Add bodies separately
        self.G = G

        self._ODEs = {}
        self.bodies = []

    
    def AddBody(self, r0 : Vector2, v0 : Vector2, m, radius = 0.1):
        """
        Adds a new Body to the group of bodies.

        Args:
        r0: initial position vector of the Body
        v0: initial velocity vector of the Body
        m: mass of the Body
        radius: radius of the Body
        """
        body = GravityBodies.Body(r0, v0, m, radius, self.G, self.bodies)
        self.bodies.append(body)
        self._ODEs[len(self._ODEs)] = body


def SimulateBodies(bodySystem : GravityBodies, dt, axislim = None):
    n = len(bodySystem.bodies)

    fig, ax = plt.subplots()

    plt.title("Planets!!")
    plt.grid()

    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    circles = []

    for i in range(n):
        circle = plt.Circle(bodySystem.bodies[i](), bodySystem.bodies[i].radius, color=np.random.choice(list('bgrcmk')))
        ax.add_patch(circle)
        circles.append(circle)

    # Set the axis limits

    # Function to update the position
    def update(frame):

        #Simulation is sped up by 100 times
        for i in range(100):
            bodySystem.forward_update(dt)

        # Calculate bounding
        com = sum([body()*body.m for body in bodySystem.bodies], Vector2(0,0))/sum([body.m for body in bodySystem.bodies])
        span = max(max([body()[0] for body in bodySystem.bodies]), max([body()[1] for body in bodySystem.bodies]))

        if axislim == None:
            ax.set_xlim(((com[0]-span)-1, (com[0]+span)+1))
            ax.set_ylim(((com[1]-span)-1, (com[1]+span)+1))
        else:
            ax.set_xlim((-axislim[0], axislim[0]))
            ax.set_ylim((-axislim[1], axislim[1]))
        ax.set_aspect('equal', adjustable='box')

        for i in range(n):
            circles[i].center = bodySystem.bodies[i]()

        return tuple(circles)

    # Create the animation object
    anim = FuncAnimation(fig, update, interval = dt*1000)

    plt.show()



def plot_bodies(gb : GravityBodies, h, total_time):
    """
    Plots the paths of the 3 bodies over time.

    Args:
    gb: a system of bodies, having exactly 3 bodies.
    total_time: the total time for which to simulate the motion of the 3 bodies
    """

    if len(gb._ODEs) != 3:
        raise ValueError("Thus function only works for 3 body systems")

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


def Q5function(positions, velocities):
    """
    Wrapper function, 
    takes list of positions and velocities of 3 bodies and plots, and simulates them.
    """
    dt = 0.001
    t = 100

    bodySystem = GravityBodies()

    bodySystem.AddBody(Vector2(*positions[0]), Vector2(*velocities[0]), 1/G, 0.1)
    bodySystem.AddBody(Vector2(*positions[1]), Vector2(*velocities[1]), 1/G, 0.1)
    bodySystem.AddBody(Vector2(*positions[2]), Vector2(*velocities[2]), 1/G, 0.1)

    plot_bodies(bodySystem, dt, t)

    bodySystem.reset()

    SimulateBodies(bodySystem, dt)
    
if __name__ == '__main__':


    # Testcase
    # A configuration I thought was fairly stable, but is not
    alpha = np.pi * 120/90

    positions = [(2,0), (-1, 2*np.sqrt(1.5)), (-1, -2*np.sqrt(1.5))]
    velocities = [tuple(0.2*Vector2(np.cos(alpha)*x - np.sin(alpha)*y, np.cos(alpha)*y + np.sin(alpha)*x)) for x,y in positions]
    Q5function(positions, velocities)


    ## uncomment for a cool solar system 
    # bodySystem = GravityBodies()
    # bodySystem.AddBody(Vector2(0,0), Vector2(0,0), 10000/G, 20)
    # bodySystem.AddBody(Vector2(0,140), Vector2(10,0), 150/G, 5)
    # bodySystem.AddBody(Vector2(0,130), Vector2(14,0), 0.01/G, 2)
    # bodySystem.AddBody(Vector2(0,400), Vector2(3,0), 1/G, 5)
    # SimulateBodies(bodySystem, 0.001, axislim=(400,400))
