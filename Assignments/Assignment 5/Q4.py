from Polynomial import Polynomial
import numpy as np
import matplotlib.pyplot as plt
from Q3 import LegendrePolynomial
from Q6 import InnerProduct
from Integral import trapizoidal_integral

f = lambda x : np.exp(x)

def LegendreBestFit(n, f, plot=True):
    """
    Find the best fit polynomial using the first n legendre polynomial
    """
    # Range is -1 to 1
    a = -1
    b = 1

    # Orthogonal set of Legendre polynomials
    phi = [LegendrePolynomial(i+1) for i in range(n)]

    # Their inner products
    C = [InnerProduct(l, l, a, b) for l in phi]

    # Value of final coefficients using equation
    A = [(1/C[i]) * InnerProduct(phi[i], f, a, b) for i in range(n)]

    # Final polynomial
    P = sum([b*a for a,b in zip(A, phi)], start=Polynomial([]))

    # Plot
    if plot:
        X = np.linspace(a, b)
        Y_f = np.vectorize(f)(X)
        Y_p = [P(x) for x in X]

        plt.title("Best fit approximation of given function using first " + str(n) + " Legendre polynomials")
        plt.plot(X, Y_f, label="Input function")
        plt.plot(X, Y_p, label="P(x)")
        plt.legend()
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    return P


if __name__ == '__main__':
    LegendreBestFit(6, f)