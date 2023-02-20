from Q1 import del_plus, del_minus, del_c, f, f_bar
import numpy as np
import matplotlib.pyplot as plt

X = np.linspace(0,1,100)

e_plus = [abs(f_bar(x) - del_plus(f, x, 0.01)) for x in X]
e_minus = [abs(f_bar(x) - del_minus(f, x, 0.01)) for x in X]
e_c = [abs(f_bar(x) - del_c(f, x, 0.01)) for x in X]

plt.plot(X, e_plus, label="Error in +")
plt.plot(X, e_minus, label="Error in -")
plt.plot(X, e_c, label="Error in c")
plt.legend()
plt.show()