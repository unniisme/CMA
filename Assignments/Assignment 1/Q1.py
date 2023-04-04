import math
import matplotlib.pyplot as plt

# Stirling's approximation function
def stirling(n):
    return math.sqrt(2*math.pi*n)*(n/math.e)**n

# Log of Stirling's approximation function
def stirlingLog(n):
    return 0.5*math.log(2*math.pi*n) + n*math.log(n/math.e)

# Standard recursive factorial function. Does not work for large n
def factorial(n):
    if n == 1:
        return n
    
    return n*fact(n-1)

# Log of factorial function
def factorialLog(n):
    fact = 0
    while n>1:
        fact += math.log(n)
        n -= 1

    return fact

# Returns a list of factorials of integers from 1 to n
def factLogList(n):
    fact = 0
    factlist = []
    for i in range(1,n):
        fact += math.log(i)
        factlist.append(fact)

    return factlist

# Generate a list of n values
n = 1000000
n_values = list(range(1, n))

# Calculate the approximation for each n value
stirling_values = [stirlingLog(n) for n in n_values]

# Factorial values
fact_values = factLogList(n)

# Plot of n vs log(n!), for actual value and approximation
plt.plot(n_values, stirling_values, label='Log of Sterling approximation')
plt.plot(n_values, fact_values, label='Log of Actual value')
plt.xlabel('n')
plt.ylabel('log(n!)')
plt.title("Stirling's Approximation for Factorials")
plt.legend()
plt.show()

# Plot of error percentage between log of approximation and log of actual value
plt.plot(n_values[1:], [100*(abs(a-s))/a for s,a in zip(stirling_values[1:], fact_values[1:])])
plt.xlabel('n')
plt.ylabel('error percentage')
plt.title("Stirling's Approximation for Factorials")
plt.show()