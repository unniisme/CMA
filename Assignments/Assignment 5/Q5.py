from Polynomial import Polynomial


def ChebyshevPolynomial(n):
    # Recursive definition of ChebyshevPolynomial

    if n==0:
        return Polynomial([1])
    if n==1:
        return Polynomial([0,1])

    return 2*Polynomial([0,1])*ChebyshevPolynomial(n-1) - ChebyshevPolynomial(n-2)  #Could use some DP!!


if __name__ == '__main__':
    print("Order 1:", ChebyshevPolynomial(1))
    print("Order 2:", ChebyshevPolynomial(2))
    print("Order 3:", ChebyshevPolynomial(3))
    print("Order 4:", ChebyshevPolynomial(4))
    print("Order 5:", ChebyshevPolynomial(5))