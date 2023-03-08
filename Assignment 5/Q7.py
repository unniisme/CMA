from Polynomial import Polynomial
import numpy as np
import matplotlib.pyplot as plt
from Q6 import InnerProduct

class FourierSeries(Polynomial):

    def __init__(self, l):
        """
        Construct a fourier series using a list of coefficients as input
        """
        if len(l) % 2 != 0:
            raise ValueError("There has to be even number of coefficients")

        self.list = l
        self.degree = len(self.list)
        self.n = self.degree//2

    def __getitem__(self, value):
        """
        Calculate the value of the fourier series at a point
        """

        trigSeries = [np.cos(i*value)*(0.5 if i==0 else 1) for i in range(self.n)] + [np.sin(i*value) for i in range(self.n)]

        return sum([x_p*c for (x_p,c) in zip(trigSeries, self.list)])

    def __str__(self):
        """
        Return the coefficients in printable format
        """
        return "Coefficients of the fourier series are:\nA : " + str(self.list[self.n:]) + "\nB : " + str(self.list[:self.n])


def FourierBestFit(n, f, f_name="", plot=True):
    """
    Find the best fit fourier series for the given function
    """
    a = -np.pi
    b = np.pi

    # Equation for coefficients
    l = [(1/np.pi)*InnerProduct(f, lambda x: np.cos(k*x), a, b) for k in range(n)] + [(1/np.pi)*InnerProduct(f, lambda x: np.sin(k*x), a, b) for k in range(n)]

    S = FourierSeries(l)

    # Plotting
    if plot:
        X = np.linspace(0, np.pi, 1000)
        Y_f = np.vectorize(f)(X)
        Y_p = [S(x) for x in X]
        plt.title("Best fit fourier series of degree "+ str(n) + " to given function " + f_name)
        plt.plot(X, Y_f, label=f_name if f_name != "" else "f(x)")
        plt.plot(X, Y_p, label="P(x)")
        plt.legend()
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    return S

f = lambda x: np.exp(x)

if __name__=='__main__':
    print(FourierBestFit(10, f, "e^x"))
    print(FourierBestFit(50, f, "e^x"))

