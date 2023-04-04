from Q1 import del_plus, del_minus, del_c, f, f_bar
import numpy as np
import matplotlib.pyplot as plt

# Sampled x values
X = np.linspace(0,1,100)

# Calculating errors in Forward, Backward and Central finite differences using the actual derivative function
e_plus = [abs(f_bar(x) - del_plus(f, x, 0.01)) for x in X]
e_minus = [abs(f_bar(x) - del_minus(f, x, 0.01)) for x in X]
e_c = [abs(f_bar(x) - del_c(f, x, 0.01)) for x in X]

plt.title("Errors in finite differences")
plt.plot(X, e_plus, label="Error in Forward Finite Difference")
plt.plot(X, e_minus, label="Error in Backward Finite Difference")
plt.plot(X, e_c, label="Error in Central Finite Difference")
plt.xlabel("x")
plt.ylabel("Error")
plt.legend()
plt.show()