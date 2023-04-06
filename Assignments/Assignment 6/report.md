# Q1
Function `forwardEulerPolynomial` uses the simple forward Euler method (Which, to note is not specific to input function. Thus this method will work for any input function f) to approximate the solution to a `y'(x) = f(x,y(x))`. The approximations are then plotted for different values of h.

# Q2
The function `Q2function` is similar to the first question, except that updation is via backward Euler method. This means this function is specific to the given ODE, but also enjoys much higher stability, as can be observed from the graphs.

# Q3
Defined general classes to handle numerical approximation of ODEs. These classes and abstract and requires inherited redefinitions depending on the ODE in question. \
- `ODE` : Class holds data about a single ODE, representing the value of a single variable at a point in time. \
Implements method for forward or backward Euler updation of the value of the function. Can be queried (called) to get the current value of the variable.
- `nODE`: Class holds data about n ODEs and their relations. Can be used to hold details about, and mass update n-Order ODEs.

Further, these classes were used to define the Pendulum ODE, which is a second order ODE.
- An ODE class each was defined for the variables ω and θ. They were defined in different manners for excercise.
- The nODE `Pendulum` simulates the updation of both these variables. Currently only uses forward updation.

The path of the pendulum is plotted in different graphs.\
Finally the function `SimulatePendulum` animates the pendulum using matplotlib.animate.

# Q4
Used ODE and nODE classes to represent the Van der Pol equation. x and v are the ODE variables.\
Used time difference between 2 consecutive maxima (averaged over 5 such differences) to calculate limit cycle.

# Q5
Class `GravityBodies(nODE)` contains data about a system of 2d bodies that apply gravity on each other. It has the subclass `Body(ODE)` which holds details about position and velocity of a single body. (Quite different from our previous implementations).

- `plot_bodies` : Plots the trajectory of a 3 body system for a given dt and total time
- `SimulateBodies` : Simulates, ie. Animates an n-body system.
- `Q5function` : Wrapper function for question statement. Takes in a list of positions and velocities for 3 bodies and constructs a system of equal mass and radius. Then plots and simulates this system.
