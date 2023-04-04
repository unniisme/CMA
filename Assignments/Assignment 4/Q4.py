import matplotlib.pyplot as plt
import numpy as np


def trapizoidal_integral(f, a, b, M):
    """
    Function that calculates, using trapizoidal approximation, the definite integral of function f in limits a and b, using M intervals.
    """
    return sum([f(a + i*(b-a)/M) + f(a + (i+1)*(b-a)/M) for i in range(M)])*(b-a)/(2*M)

def f(x):
    ## Question function
    return 2*x*np.exp(x**2)

def F(x):
    ## Indefinite integral of question function
    return np.exp(x**2)


if __name__ == '__main__':

    # Plotting
    Ms = list(range(100,1000))
    I = [trapizoidal_integral(f, 1, 3, M) for M in Ms]
    Y_true = [F(3)-F(1) for M in Ms]


    plt.plot(Ms, I, label="Trapezoidal approximation")
    plt.plot(Ms, Y_true, label="True value of integral")
    plt.legend()
    plt.title("Variation of trapizoidal approximation with number of intervals")
    plt.xlabel("Number of intervals M")
    plt.ylabel("Integral value")
    plt.show()