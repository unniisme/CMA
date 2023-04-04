import random
import matplotlib.pyplot as plt
import math

def estimatePi(samples):
    sqCount = 0
    cirCount = 0
    ratios = []

    # For each sample
    for i in range(samples):
        # Take random points with x coordinate and y coordinate randomly sampled from a uniform probability distribution between -0.5 and 0.5
        pt = (random.uniform(-0.5,0.5), random.uniform(-0.5,0.5))

        # If the selected point lies within the unit circle centered around origin, keep count
        if (pt[0]**2 + pt[1]**2) <= 0.5**2:
            cirCount += 1
        # Keep count of total number of points
        sqCount += 1

        # 4*ratio between the 2 kind of points converges to the value of pi
        ratios.append(4*cirCount/sqCount)

    # Plot the value and return
    plt.plot(ratios, label='Estimation')
    plt.plot([math.pi]*len(ratios), label='Value of math.pi')
    plt.xlabel('Number of random samples')
    plt.ylabel('4*Fraction of points within the circle')
    plt.title("Estimation of π using Monte Carlo Method")
    plt.legend()
    plt.show()

    print("Final estimate for pi: ", 4*cirCount/sqCount)

## Test case
# estimatePi(2000000)