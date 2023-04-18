import numpy as np
import matplotlib.pyplot as plt

def Newton_Raphson(F, J, M, X0, plot=False):
    """
    F : Multivariate function
    J : Jacobian as a function
    M : number of iterations
    X0 : Initial value of X

    returns Roots of F estimated using Newton-Raphson method
    """
    X = X0

    if plot:
        iterations = []
        modulus = []

    for i in range(M):
        X = X - np.linalg.inv(J(X)) @ F(X).T

        if plot:
            iterations.append(i)
            modulus.append(np.linalg.norm(F(X)))

    if plot:
        plt.plot(iterations, modulus)
        plt.xlabel('Number of iterations')
        plt.ylabel('∥F(X)∥')
        plt.title('Convergence of Newton-Raphson Method')
        plt.show()

    return X

if __name__ == '__main__':

    f1 = lambda X: 3*X[0] - np.cos(X[1]*X[2]) - (3/2)
    f2 = lambda X: 4*(X[0]**2) - 625*(X[1]**2) + 2*X[2] - 1
    f3 = lambda X: 20*X[2] + np.exp(-X[0]*X[1]) + 9

    # Multivariate function
    F = lambda X: np.array([f1(X), f2(X), f3(X)])

    # Jacobian of F
    J = lambda X: np.array([
        [3,                         X[2]*np.sin(X[1]*X[2]),     X[1]*np.sin(X[1]*X[2])  ],

        [8*X[0],                   -1250*X[1],                 2                       ],

        [-X[1]*np.exp(-X[0]*X[1]), -X[0]*np.exp(-X[0]*X[1]),    20                      ]
    ])

    X = Newton_Raphson(F, J, 50, np.array([1,1,1]), plot=True)
    print("X =", X)

    print("F(X) =", F(X))