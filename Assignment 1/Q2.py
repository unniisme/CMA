from random import random
import matplotlib.pyplot as plt

class Dice:

    # Construct a dice
    def __init__(self, sides = 6):
        
        # Construct n sided dice, throws error for datatype mismatch or number of sides of die is less than 4
        if type(sides) != int or sides < 4:
            raise Exception("Cannot construct the dice")
        self.sides = sides

        # Initial probability distribution is uniform for all sides
        self.pd = [1/self.sides] * self.sides
        self.calculateCDF()

    def __str__(self):
        # Pretty printing
        return "A dice with " + str(self.sides) + " sides and probability distribution " + str(self.pd)

    def setProb(self, probs):
        # Redefine probability distribution
        # Throws error if not all values of the distribution are defined, or if the probabilities don't add upto 1
        if len(probs) != self.sides or sum(probs) != 1:
            raise Exception("Invalid probability distribution")
        self.pd = list(probs)
        self.calculateCDF()


    def calculateCDF(self):
        # Function to calculate cumulated probability distribution for each side
        self.cdf = [0]
        for p in self.pd:
            self.cdf.append(p+self.cdf[-1])


    def roll(self, n, barWidth=0.4):
        # Randomly roll n dice with the given probability distribution and plot a graph comparing it with the expected values
        expected = [n*i for i in self.pd]
        obtained = [0] * self.sides

        # Rolling is done by generating a randon number between 0 and 1 and finding the range in cdf where it falls
        for i in range(n):
            roll = random()
            for i in range(self.sides):
                if self.cdf[i+1] > roll > self.cdf[i]:
                    obtained[i] += 1

        # print(expected)
        # print(obtained)

        #Plotting
        plt.bar(range(self.sides), expected, barWidth, label='Expected')
        plt.bar([i+0.4 for i in range(self.sides)], obtained, barWidth, label='Actual')
        plt.xticks([r + barWidth/2 for r in range(self.sides)], [i+1 for i in range(self.sides)])
        plt.xlabel('Sides')
        plt.ylabel('Occurrences')
        plt.title('Outcome of ' + str(n) + ' throws of ' + str(self.sides) + ' sided dice')
        plt.legend()
        plt.show()


## Test cases
# a = Dice(4)
# a.setProb((0.1, 0.2, 0.3, 0.4))
# a.roll(10000)

# a = Dice(6)
# a.roll(100)