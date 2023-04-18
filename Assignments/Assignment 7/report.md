# Q1
`HeatEquation1D` represents the one-dimensional heat equation.  
The PDE per step is simulated using `forward_euler`, which uses a matrix equation to update the discretised values of temparature on the 1D rod.  
`forward_euler_iterative` does the same using iterative procedures. The other function is used as it will be faster.

# Q2
`HeatEquation2D` represents the 2D heat equation.  
`forward_euler` does forward update iteratively on each grid cell.  
 Boundary conditions are applied on the first and last rows and columns of the grid.  
The result is visualised using `matplotlib` `animation` and `imshow` methods.

# Q3
This code calculates the nth root of a positive real number a, with a given error tolerance ɛ. The algorithm uses binary search to converge on the solution.  
Error is within ɛ as difference between consecutive values of estimated roots is less than ɛ.  
The worst-case runtime complexity of this algorithm is O(log(a/ε)), since the algorithm halves the search space with each iteration of the loop. Assuming a is a constant, runtime complexity of this algorithm is O(log(1/ε)).

# Q4
Newton-Raphson and Secant methods for 1D functions are implemented trivially, with convergence criteria also in place.  
Their convergence rate is compared using number of steps required to converge to a root from the same initialisation, against different input functions.

# Q5
Newton-Raphson method is implemented for multi dimensional functions. Note that the Jacobian has to also be inputted as a matrix function for this to work.  
The answer is printed and convergence rate is plotted.

# Q6
Aberth method is implemented.  
It is to note that the output values depend on an input approximation. The input approximations have to be distinct values. They should be complex if complex roots are also to be found. It may also be noted that it if one can provide less then the number of root values as input, which will cause only those many roots to be found.

# Q7
For an input function, first some very approximate values of roots are found using places where the function switches signs.  
Then using the enhanced polynomial class, a good fit polynomial for the given function is found. This found poynomial has a degree a constant greater than the expected number of zeroes. This is to ensure that the polynomial is a good enough approximation without being redundantly large.  
Finally, the approximated roots are used as input to Aberth method on the found polynomial to approximate a much more sharper approximation of each of these roots.