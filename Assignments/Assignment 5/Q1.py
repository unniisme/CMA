from Polynomial import Polynomial
import matplotlib.pyplot as plt
import numpy as np

def BestFitPoly(n, pts, plot=True):
    x = [pt[0] for pt in pts]
    y = [pt[1] for pt in pts]

    X = np.zeros((len(x), n+1))

    # Generate a matrix with x**i as each column
    for i in range(n+1):
        X[:,i] = np.array(x)**i

    # Use linsolve to solve the system of linear equations for the coefficients.
    coeffs = np.linalg.solve(X.T @ X, X.T @ y)

    # Construct a polynomial with the coefficients
    p = Polynomial(list(coeffs))

    X_plot = np.linspace(min(x),max(x), 100)
    Y_plot = [p[i] for i in X_plot]

    if plot:
        plt.title("Best fit polynomial of degree " + str(n) + " on given points")
        plt.scatter(x, y, c="r")
        plt.plot(X_plot, Y_plot)
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.show()

    return p

if __name__=='__main__':
    inputpts= [(0,0), (-4,-3),  (1,-2), (-5,-4), (-2,-2), (2,-2)]
    print("Input points: ", inputpts)
    print("Degree 4")
    print(BestFitPoly(4, inputpts))
    print("Degree 7")
    print(BestFitPoly(7, inputpts))
