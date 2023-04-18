from Polynomial import Polynomial, BestFitPolyFunction
import numpy as np
import Q6

def roots(f, a, b):
    """
    Find approximate roots of a function using Aberth method.

    Parameters:
    f : ℝ → ℝ
    interval (a,b)

    Returns the approximate roots of f in the interval [a, b].
    """

    M = int((b-a)*100)

    x_prev = a
    X0 = []
    # Find very approximate values of roots which will further approximated by Aberth method
    for x in np.linspace(a,b,M):
        if f(x_prev) * f(x) <= 0:
            X0.append(x)
        x_prev = x

    # Approximate the function using a polynomial 5 degrees higher than number of estimated roots.
    ## This is because if number of approximated roots is too small, the polynomial approximation may be inaccurate
    P = BestFitPolyFunction(len(X0)+5, f, a, b, M)

    return P.printRoots(X0)

if __name__ == '__main__':


    print("x³ - 6x² + 11x - 6")
    print("Intervel [-5, 5]")
    f = lambda x: x**3 - 6*x**2 + 11*x - 6
    X = roots(f, -5, 5)
    X_actual = [1, 2, 3]
    print("calculated roots :", X)
    print("actual roots:", X_actual)
    print("f(X): ", [f(x) for x in X])

    print()
    print("sin(x)")
    print("Intervel [-4, 4]")
    f = lambda x: np.sin(x)
    X = roots(f, -4, 4)
    X_actual = [-np.pi, 0, np.pi]
    print("calculated roots :", X)
    print("actual roots:", X_actual)
    print("f(X): ", [f(x) for x in X])

    print()
    print("2^x - 3") 
    print("Intervel [-5, 5]")
    f = lambda x: 2**x - 3 
    X = roots(f, -5, 5) 
    X_actual = [np.log2(3)]
    print("calculated roots :", X)
    print("actual roots:", X_actual)
    print("f(X): ", [f(x) for x in X])
    
