from scipy import integrate
from Q4 import f, F
import numpy as np
import matplotlib.pyplot as plt


X = np.linspace(0,20,100)
I_quad = [integrate.quad(f, 0, x) for x in X]
# I_trapezoid = [integrate.trapezoid(f, 0, x) for x in X]
# I_ctrap = [integrate.cumulative_trapezoid(f, 0, x) for x in X]
I_simpson = [integrate.simpson(f, 0, x) for x in X]
I_romb = [integrate.romb(f, 0, x) for x in X]
I_true = [F(x) - F(0) for x in X]


plt.plot(X, I_quad)
# plt.plot(X, I_trapezoid)
# plt.plot(X, I_ctrap)
plt.plot(X, I_simpson)
plt.plot(X, I_romb)
plt.plot(X, I_true)