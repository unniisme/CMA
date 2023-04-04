from Polynomial import Polynomial
import Q6
import numpy as np
import matplotlib.pyplot as plt

# Question function
f = lambda x: np.exp(x) * np.sin(x)

# Anti derivative of f
F = lambda x: np.exp(x) * (np.sin(x) - np.cos(x)) * 0.5

# Sampling 14 points between 0 and 1/2
X = np.linspace(0, 0.5, 14)
pts = list(zip(list(X), list(np.vectorize(f)(X))))
p = Polynomial([])

# Curve fitting a 14 degree polynomial onto these points
p = p.fitViaMatrixMethod(pts, showPlot=False)

# Comparison
print("Area obtained Via Polynomial: ", p.area(0,0.5))
print("Actual Area: ", F(0.5) - F(0))
print("Error: ", F(0.5) - F(0) - p.area(0,0.5))

# Plot
X_full = np.linspace(0,0.5,100)
plt.plot(X_full, [p[x] for x in X_full], label="Polynomial approximation")
plt.plot(X_full, [f(x) for x in X_full], label="Actual function")
plt.title("Polynomial approximation of exp(x) * sin(x) in the range [0,1/2]")
plt.legend()
plt.xlabel("x")
plt.ylabel("f(x)")
plt.show()

