import numpy as np
import matplotlib.pyplot as plt


def del_plus(f, x, h):
    return (f(x+h) - f(x))/h

def del_minus(f, x, h):
    return (f(x) - f(x-h))/h

def del_c(f, x, h):
    return (f(x+h) - f(x-h))/(2*h)

def f(x):
    return np.sin(x**2)

def f_bar(x):
    return 2*x*np.cos(x**2)

if __name__=='__main__':
    X = np.linspace(0,1,100)
    Y_true = np.vectorize(f_bar)(X)
    Y_del = np.vectorize(lambda x: del_plus(f, x, 0.01))(X)

    plt.plot(X, Y_true, label="Actual derivative")
    plt.plot(X, Y_del, label="Forward Finite Approximation")
    plt.legend()
    plt.show()