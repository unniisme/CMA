def trapizoidal_integral(f, a, b, M):
    """
    Function that calculates, using trapizoidal approximation, the definite integral of function f in limits a and b, using M intervals.
    """
    return sum([f(a + i*(b-a)/M) + f(a + (i+1)*(b-a)/M) for i in range(M)])*(b-a)/(2*M)
