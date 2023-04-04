from Q1 import del_plus, del_minus, del_c, f, f_bar
import numpy as np
import matplotlib.pyplot as plt

def get_max_error(f, f_bar, del_, h, x_range):
    """
    Function that returns the maximum error in a finite difference given h and a range of x
    """
    return max([abs(f_bar(x) - del_(f, x, h)) for x in x_range])

def f_double_bar(x):
    # Second derivative of the question function
    return 2*np.cos(x**2) - 4*np.sin(x**2)*(x**2)

def f_triple_bar(x):
    # Third derivative of the question function
    return -12*x*np.sin(x**2)-8*np.cos(x**2)*(x**3)

def theoretical_absolute_error_plus_f(h):
    # Function that calculates the theoretical maximum aboslute error for forward finite difference given h and x in range [0,1] 
    etas = np.linspace(0,1+h, 100)
    return max([abs(h*f_double_bar(x)/2) for x in etas])

def theoretical_absolute_error_central_f(h):
    # Function that calculates the theoretical maximum aboslute error for central finite difference given h and x in range [0,1] 
    X = np.linspace(0,1,10)
    maxs = []
    for x in X:
        # maxs += [abs(((h**2)/6) * (f_triple_bar(x_1) + f_triple_bar(x_2))) for x_1 in np.linspace(x-h, x, 10) for x_2 in np.linspace(x, x+h, 10)]
        maxs += [abs((h/4) * (f_double_bar(x_1) - f_double_bar(x_2))) for x_1 in np.linspace(x-h, x, 10) for x_2 in np.linspace(x, x+h, 10)]
    return max(maxs)

# Plotting
H = np.linspace(0,1,100)
X = np.linspace(0,1,100)

plt.plot(H, [get_max_error(f, f_bar, del_plus, h, X) for h in H], label = "Max error in Forward Finite Approximation")
plt.plot(H, [theoretical_absolute_error_plus_f(h) for h in H], label = "Theoretical max error in Forward Finite Approximation") 
plt.plot(H, [get_max_error(f, f_bar, del_c, h, X) for h in H], label = "Max error in Central Finite Approximation")
plt.plot(H, [theoretical_absolute_error_central_f(h) for h in H], label = "Theoretical max error in Central Finite Approximation") 
plt.legend()
plt.title("Variation of error in finite approximations wrt h")
plt.xlabel("h")
plt.ylabel("Max Error")
plt.show()