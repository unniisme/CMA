from Polynomial import Polynomial
import numpy as np
from Q5 import ChebyshevPolynomial
from Integral import trapizoidal_integral

fp_precision = 10e-6

def InnerProduct(phi_1 : "function", phi_2 : "function", a, b, w : "function" = lambda x:1, M=1000):
    """
    Calculates the inner product of functions phi_1 and phi_2 wrt weight function w in intervel [a,b] using trapizoidal_integral approximation
    """
    I = trapizoidal_integral(lambda x: phi_1(x)*phi_2(x)*w(x),a, b, M)
    return I


if __name__ == '__main__':

    # First 5 Chebyshev Polynomials
    P = [ChebyshevPolynomial(1), ChebyshevPolynomial(2), ChebyshevPolynomial(3), ChebyshevPolynomial(4), ChebyshevPolynomial(5)]

    w = lambda x: 1/np.sqrt(1-x**2) if abs(x)!= 1 else 0  # Weight function for inner product

    print("Numerical approximations of inner products of Chebyshev Polynomials upto first 5")

    ar = np.zeros((5,5))

    ## Evaluate inner product for each pair
    for i, phi_i in enumerate(P):
        for j, phi_j in enumerate(P):
            print()
            print(str(i+1) + "th and " + str(j+1) + "th Chebyshev Polynomial")
            orth = InnerProduct(phi_i, phi_j, -1, 1, w, 100000)
            print("I = " , orth, "~", round(orth, 2))
            ar[i,j] = round(orth, 4)

    print()
    print("Summary:")
    print(ar)
