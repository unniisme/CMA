from Polynomial import Polynomial

def derivative(poly):
    """
    Function to calculate the derivative of a polynomial
    """
    newP = []
    for i,c in enumerate(poly.list):
        if i!=0:
            newP.append(i*c)

    return Polynomial(newP)

Polynomial.derivative = derivative

def area(poly, a, b):
    """
    Function to calculate the definite integral of a polynomial in the given range.
    """
    newP = [0]
    for i,c in enumerate(poly.list):
        newP.append(c/(i+1))

    newP = Polynomial(newP)
    return newP[b] - newP[a]

Polynomial.area = area


if __name__ == '__main__':
    # Test cases
    p = Polynomial([1, 2, 3])
    pd = p.derivative()
    print(pd)

    p = Polynomial([1, 2, 3])
    print(p.area(1,2))