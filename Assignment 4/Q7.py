from Polynomial import Polynomial
import Q6
import numpy as np
import matplotlib.pyplot as plt

f = lambda x: np.exp(x) * np.sin(x)

X = np.linspace(0, 0.5, 100)
pts = list(zip(list(X), list(np.vectorize(f)(X))))
p = Polynomial([])
p.fitViaMatrixMethod(pts)

plt.plot(X, [p[x] for x in X])
plt.show()