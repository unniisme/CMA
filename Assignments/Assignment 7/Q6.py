from Polynomial import Polynomial

def aberth_method(P : Polynomial, ɛ, Z):
    """
    Computes the roots of a polynomial P using Aberth's method

    Parameters:
        P (Polynomial): The polynomial of degree n
        ɛ (float): The error tolerance
        Z (list): The initial guesses for the roots. 
            Note that Z has to be of size less than or equal to degree of P - 1

    Returns:
        A list of approximate roots of P
    """
    n = min(P.degree-1, len(Z))

    if n==0:
        return None

    Z0 = [z+10*ɛ for z in Z]


    while any([abs(Z[i] - Z0[i])>ɛ for i in range(n)]):
        """
        for all k
        z_k(t+1) = z_k(t) - 1/(P'(z_k(t))/P(z_k(t)) - sum(z_k - z_j for all j, k != j))

        halts when change in each root estimate is less than ɛ.
        """
        memo = [sum([1/(Z[k] - Z[j])  if j!=k else 0 for j in range(n)]) for k in range(n)]
        Z0 = Z.copy()
        for i in range(n): 
            t = P(Z[i])/P.derivative()(Z[i])
            Z[i] -= t/(1 - t*memo[i])

    return Z

Polynomial.printRoots = lambda self,Z0: aberth_method(self, 10e-3, Z0)


if __name__ == '__main__':

    # Test case 1: p1 has two real roots
    p1 = Polynomial([-1, 0, 1])
    print("x² - 1")
    print(p1.printRoots([-2, 0.5]))
    print()
    # expected output: "-1.000, 1.000"

    # Test case 2: p2 has one repeated root
    p2 = Polynomial([1, -4, 4])
    print("4x² - 4x + 1")
    print(p2.printRoots([0, 1]))
    print()
    # expected output: "0.500, 0.500"

    # Test case 3: p3 has three real roots
    p4 = Polynomial([1, -6, 11, -6])
    print("-6x³ + 11x² - 6x + 1")
    print(p4.printRoots([-1, 0, 1]))
    print()
    # expected output: "1.000, 0.500, 1.000"

    # Test case 5: p5 is a constant function
    p5 = Polynomial([5])
    print("5")
    print(p5.printRoots([]))
    print()
    # expected output: "No roots found."

    # Test case 6: p6 is a linear polynomial
    p6 = Polynomial([0,1])
    print("x")
    print(p6.printRoots([1]))
    print()

    # Test case 7: complex roots
    p7 = Polynomial([1,0,1])
    print("x² + 1")
    print(p7.printRoots([complex(1,1),complex(2,2)]))
