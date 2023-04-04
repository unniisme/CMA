from Q1 import BestFitPoly
import numpy as np
import matplotlib.pyplot as plt

f = lambda x: np.sin(x) + np.cos(x)

def BestFitPolyFunction(n, f, f_name = "", plot=True):
    ## Applies BestFitPoly on a function, simply takes many points of the function and runs BestFitPoly on thsoe points
    X = np.linspace(0, np.pi, 5*n)

    pts = [(x, f(x)) for x in X]

    p = BestFitPoly(n, pts, plot=False)


    if plot:
        X = np.linspace(0, np.pi, 1000)
        Y_f = np.vectorize(f)(X)
        Y_p = [p[x] for x in X]
        plt.title("Best fit polynomial of degree "+ str(n) + " to given function " + f_name)
        plt.plot(X, Y_f, label=f_name if f_name != "" else "f(x)")
        plt.plot(X, Y_p, label="P(x)")
        plt.legend()
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    return p


if __name__ == '__main__':
    print(BestFitPolyFunction(2, f, "sin(x)+cos(x)"))
    print(BestFitPolyFunction(3, f, "sin(x)+cos(x)"))
    print(BestFitPolyFunction(7, f, "sin(x)+cos(x)"))
    print(BestFitPolyFunction(15, f, "sin(x)+cos(x)"))

