from Q1 import RowVectorFloat
from Q2 import SquareMatrixFloat

import numpy as np
import matplotlib.pyplot as plt

## Testing Jacobi Method and Gauss-Siedel method on the following linear system:
"""
A =
2   -1  1   1
0   1  0   0
1   2  4  -2
-6  4   3   8

b = 1 -1 0 1
"""
A = [[2,-1,1,1],[0,1,0,0],[1,2,4,-2],[-6,4,3,8]]
b = [1,-1,0,1]

## Calculting actualy solution using x = A_inv*b 
expected_x = np.linalg.inv(np.array(A))@np.array(b)

## Running both methods
m = 50
m_A = SquareMatrixFloat(4,A)
e_j, x_j = m_A.jSolve(b, m)
e_gs, x_gs = m_A.gsSolve(b, m)

print("Expected value of x: ", expected_x)
print("Value of x from Jacobi method: ", x_j)
print("Value of x from Gauss-Siedel method: ", x_gs)

## Plotting
plt.plot([i for i in range(m)], e_j, label="Error in Jacobi method")
plt.plot([i for i in range(m)], e_gs, label="Error in Gauss-Siedel method")
plt.title("Convergence of Jacobi and Gauss-Siedel methods")
plt.xlabel("Number if iterations")
plt.ylabel("||Ax-b||")
plt.legend()
plt.show()