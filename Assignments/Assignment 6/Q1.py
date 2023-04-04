import numpy as np
from Polynomial import Polynomial, BestFitPoly
import matplotlib.pyplot as plt

def forwardEulerPolynomial(f, y0, x0, x1, h):
    """
    y'(x) = f(x,y(x))

    y(x+h) = h*f(x,y(x))    

    returns a polynomial that best fits the given parameters
    """
    y = y0
    x = x0

    X = [x0]
    Y = [y0]

    while x<x1:
        y = y + h*f(x,y)
        x = x + h
        Y.append(y)
        X.append(x)

    return BestFitPoly(int((x1-x0)/h), X, Y)

def f(t,x):
    return -2*x

def F(t):
    return 5*np.exp(-2*t)

def PlotForh(f, x0, t0, t1, h):
    # Wrapper function cos I'm lazy
    T = np.arange(t0,t1,h)
    
    P = forwardEulerPolynomial(f, x0, t0, t1, h)
    plt.plot(T, [P(t) for t in T], label=str(h))

if __name__ == '__main__':
    t0 = 0
    t1 = 10
    x0 = 5

    # Case 1, h = 0.1
    PlotForh(f, x0, t0, t1, 0.1)

    # Case 2, h = 0.5
    PlotForh(f, x0, t0, t1, 0.5)

    # Case 3, h = 1
    PlotForh(f, x0, t0, t1, 1)

    # Case 4, h = 2
    PlotForh(f, x0, t0, t1, 2)

    # Case 4, h = 3
    PlotForh(f, x0, t0, t1, 3)
    
    T = np.linspace(0,5, 1000)
    plt.plot(T, np.vectorize(F)(T), label="Actual")
    plt.legend()
    plt.show()

