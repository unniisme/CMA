from Polynomial import Polynomial
import math
import numpy as np

def LegendrePolynomial(n):
    if n==0:
        return Polynomial([])

    # Direct equation for Legendre polynomial
    # Note that power of polynomial as well as nth derivative has been implemented in the Polynomial class in Polynomial.py
    return (Polynomial([-1,0,1])**n).derivative(n) * (1/(np.exp2(n)*math.factorial(n)))


if __name__ == '__main__':
    print("Order 1:", LegendrePolynomial(0))
    print("Order 2:", LegendrePolynomial(1))
    print("Order 3:", LegendrePolynomial(2))
    print("Order 4:", LegendrePolynomial(3))
    print("Order 5:", LegendrePolynomial(4))
    print("Order 7:", LegendrePolynomial(5))
    print("Order 8:", LegendrePolynomial(6))