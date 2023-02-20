import matplotlib.pyplot as plt
import numpy as np



def trapizoidal_integral(f, a, b, M):
    return sum([f(a + i*(b-a)/M) + f(a + (i+1)*(b-a)/M) for i in range(M)])*(b-a)/(2*M)

def f(x):
    return 2*x*np.exp(x**2)

def F(x):
    return np.exp(x**2)


if __name__ == '__main__':
    Ms = list(range(100,1000))
    I = [trapizoidal_integral(f, 1, 3, M) for M in Ms]
    Y_true = [F(3)-F(1) for M in Ms]


    plt.plot(Ms, I)
    plt.plot(Ms, Y_true)
    plt.show()