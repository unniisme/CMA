import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation 
from scipy import interpolate
import random as rn

# Define plot
fig = plt.figure() 
axis = plt.axes(xlim = (-0.02,1.02), ylim =(-4, 4)) 
  
# Define each graph
line_true, = axis.plot([], [], lw = 2)
line_cs, = axis.plot([], [], lw = 2)
line_akima, = axis.plot([], [], lw = 2)
line_bary, = axis.plot([], [], lw = 2)

lines = [line_true, line_cs, line_akima, line_bary]
   
# Function in picture
def objective_function(x):
    return np.tan(x)*np.sin(30*x)*np.exp(x)

# Define the range of x and find true value of y
x_linspace = np.linspace(0,1,100)
y_true = [objective_function(x) for x in x_linspace]

# Plot initialization
plt.grid()
line_true.set_label("True")
line_cs.set_label("Cubic Spline")
line_akima.set_label("Akima")
line_bary.set_label("Barycentre")
plt.legend(loc="upper left")
plt.xlabel("x")
plt.ylabel("f(x)")


def init(): 
    # Animation initialization
    [line.set_data([], []) for line in lines]
    return lines 
   
# animation function 
def animate(i):

    # Random sampling
    i = i+2
    x_sampled = sorted(rn.sample(list(x_linspace), i))
    y_sampled = [objective_function(x) for x in x_sampled]

    # Define each interpolation model
    cs = interpolate.CubicSpline(x_sampled, y_sampled)
    akima = interpolate.Akima1DInterpolator(x_sampled, y_sampled)
    bary = interpolate.BarycentricInterpolator(x_sampled, y_sampled)

    # Calculate interpolated values
    y_cs = cs(x_linspace)
    y_akima = akima(x_linspace)
    y_bary = bary(x_linspace)
    
    # Draw each graph
    line_true.set_data(x_linspace, y_true)
    line_cs.set_data(x_linspace, y_cs)
    line_akima.set_data(x_linspace, y_akima)
    line_bary.set_data(x_linspace, y_bary)

    # Update title
    plt.title("Interpolations of tan(x) sin(30x) eˣ for "+ str(i) + " samples")
      
    return lines
   
# call the animation function     
anim = FuncAnimation(fig, animate, init_func = init, 
                               frames = 40) 
   
# Show animation
plt.show()
