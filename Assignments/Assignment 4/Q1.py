import numpy as np
import matplotlib.pyplot as plt


def del_plus(f, x, h):
    """Forward finite difference for function f, given x and h"""
    return (f(x+h) - f(x))/h

def del_minus(f, x, h):
    """Backward finite difference for function f, given x and h"""
    return (f(x) - f(x-h))/h

def del_c(f, x, h):
    """Central finite difference for function f, given x and h"""
    return (f(x+h) - f(x-h))/(2*h)

def f(x):
    ## Question function
    return np.sin(x**2)

def f_bar(x):
    ## first derivative of f
    return 2*x*np.cos(x**2)

if __name__=='__main__':
    X = np.linspace(0,1,100)                                    # Sample x values
    Y_true = np.vectorize(f_bar)(X)                             # True derivative values
    Y_del = np.vectorize(lambda x: del_plus(f, x, 0.01))(X)     # Calculated forward finite difference values

    # Plot
    plt.plot(X, Y_true, label="Actual derivative")
    plt.plot(X, Y_del, label="Forward Finite Approximation")
    plt.title("Forward Finite Difference and actual derivative")
    plt.xlabel('x')
    plt.ylabel("f'(x)")
    plt.legend()
    plt.show()