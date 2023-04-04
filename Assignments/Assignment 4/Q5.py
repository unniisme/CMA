from scipy import integrate
from Q4 import f, F
import numpy as np
import matplotlib.pyplot as plt

# X spaces
N = 500
X = np.linspace(0,2,N)
Y = [f(x) for x in X]

# Integral using various methods in Scipy
I_quad = [integrate.quad(f, 0, x)[0] for x in X]
I_trapezoid = [0] + [integrate.trapezoid(Y[:i], X[:i]) for i in range(1,N)]
I_simpson = [0] + [integrate.simpson(Y[:i], X[:i]) for i in range(1,N)]
I_true = [F(x) - F(0) for x in X]

# Plotting
plt.title("Area under the curve 2x · exp(x²) in intervel [0,u] using various methods")
plt.xlabel("u")
plt.ylabel("I")
plt.plot(X, I_quad, label="Quad")
plt.plot(X, I_trapezoid, label="Trapezoid")
plt.plot(X, I_simpson, label="Simpson")
plt.plot(X, I_true, label="True")
plt.legend()
plt.show()