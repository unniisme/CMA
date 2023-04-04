# Q1
Plotting the finite differences are fairly trivial. \
`del_plus(f,x,h)` : Function that returns the forward finite difference for function f at x, given the value of h. \
`del_minus` and `del_c` are the corresponding functions for backward finite difference and central finite difference.

# Q2
Errors for each finite difference can be calculated by subtracting the value of the finite difference from the actual value of the derivative. The actual value of the derivative is calcuated by pen and paper and implemented as `f_bar` (`f` being the function itself).

# Q3
Maximum error for a given h is calculated as the maximum of errors over all x in range [0,1] for each finite difference. \
The Theoretical maximum error is calculated using the second derivative `f_double_bar`. This is as per the error derivations for the corresponding function. The maximum error in the corresponding intervals of zeta are taken in each of these cases.

# Q4
`trapizoidal_integral(f,a,b,M)` : Function that uses trapizoidal method to approximate the definite integral of function f in limits a and b, using M intervals.

# Q5
The following scipy methods were visualised: \
`quad`, `Trapezoid`, `Simpson`. The true values were also plotted.

# Q6
`derivative` : Method that on input of a polynomial, returns its derivative. This is done by taking terms of each degree and multiplying the coefficients with the degree-1.
`area` : Method that takes in a polynomial and a range and returns the area under the curve for that range. This is done by taking the anti derivative first. The anti derivative is calculated by taking each degree and dividing the coefficient by the degree itself. Then the definite integral is directly calculated by subtituting.

# Q7
The givem function is sampled uniformly for 14 points and a polynomial that fits these points are found using the fitViaMatrixMethod that we have defined in the previous assignment. The area under this approximated polynomial is then found using the `area` method defined in the previous question. 