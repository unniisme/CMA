from Vector import RowVectorFloat
import matplotlib.pyplot as plt
import numpy as np

class Polynomial(RowVectorFloat):

    # powerDict = {0:'⁰', 1:'¹', 2:'²', 3:'³', 4:'⁴', 5:'⁵', 6:'⁶', 7:'⁷', 8:'⁸', 9:'⁹'}  ## Just an attempt to show powers well

    def __init__(self, l):
        """
        Construct a polynomial using a list of coefficients as input
        """
        self.list = l
        self.degree = len(self.list)      
        
        ## Take care of trailing zeroes
        self.truncate()

    def __str__(self):
        """
        Return the coefficients in printable format
        """
        return "Coefficients of the polynomial are:\n" + super().__str__()

    def __repr__(self):
        """
        Shell representation
        """
        return self.__str__()


    def __add__(self, other):
        """
        Add 2 polynomials
        """
        # Adjust degree accordingly so that polynomials of different degress can be added
        if self.degree > other.degree:
            other.list += [0]*(self.degree - other.degree)
            other.degree = self.degree
        if self.degree < other.degree:
            self.list += [0]*(other.degree - self.degree)
            self.degree = other.degree

        # call super class method
        return Polynomial(super().__add__(other).list)

    def __sub__(self, other):
        """
        Subtract 2 polynomials
        """
        return self + (-1)*other

    def __mul__(self, other):
        """
        Multiply 2 polynomials, or a polynomial and a constant
        """

        if isinstance(other, Polynomial):
            newP = [0] * (self.degree + other.degree)
            # Go through each term of each polynomial and multiply them. Put them in the correct degree.
            for i,val1 in enumerate(self.list):
                for j,val2 in enumerate(other.list):
                    newP[i+j] += val1*val2

            return Polynomial(newP)
                
        
        return Polynomial(super().__mul__(other).list)

    def __rmul__(self, other):
        return Polynomial(super().__rmul__(other).list)

    def __getitem__(self, value):
        """
        Evaluate polynomial
        """
        powerSeries = [value**i for i in range(self.degree)]

        return sum([x_p*c for (x_p,c) in zip(powerSeries, self.list)])

    def truncate(self):
        """
        Remove trailng 0 coefficients
        """
        if len(self.list) <= 1:
            return
        while self.list[-1] == 0 and len(self.list) > 1:
            self.list.pop(-1)
        self.degree = len(self.list)

    def asString(self):
        """
        The algebraic representation of the polynomial
        """
        s = ""
        for i,c in enumerate(self.list):
            if c>=0:
                if i!=0:
                    s+="+"
                s += str(c)
            else:
                if i!=0:
                    s+="-"
                s += str(-c)
            s += "(x^" + str(i) + ")"
        return s

    def show(self, a = 0, b = 1):
        """
        Plot the polynomial in the given intervel
        """    
        numpts = 100

        X = np.linspace(a,b, numpts)

        Y = [self[x] for x in X]

        plt.plot(X,Y)
        plt.title("Plot of Polynomial " + self.asString())
        plt.xlabel("x")
        plt.ylabel("P(x)")
        plt.grid()
        plt.show()

    def fitViaMatrixMethod(self, l):
        """
        Find a polynomial that fits the given list of points using matrix inverse
        """
        input_x = np.array([x for x,y in l])

        # Generate the matrix that represents the polynomials for each x
        A = np.array([1]*len(l))
        for i in range(len(l)-1):
            A = np.c_[A, input_x**(i+1)]
    
        b = np.array([y for x,y in l])

        ## Ax = b
        ## Solve x = A_inv*b
        try:
            X = np.linalg.inv(A) @ b
        except:
            raise Exception("Equation unsolvable")
        self = Polynomial(list(X))

        ## Plot
        numpts = 100

        X = np.linspace(min(input_x),max(input_x), numpts)

        Y = [self[x] for x in X]

        plt.plot(X,Y)
        plt.scatter(input_x, b, c='r')
        plt.title("Polynomial interpolation using matrix method")
        plt.xlabel("x")
        plt.ylabel("P(x)")
        plt.grid()
        plt.show()

    def fitViaLagrangePoly(self, l):
        """
        Find a polynomial that fits the given list of points using lagrange polynomials
        """
        n = len(l)
        X = [x for x,y in l]
        Y = [y for x,y in l]

        def psi(j):
            """
            Function to calculate the lagrange polynomial for jth x
            """
            pi = 1
            for i in range(n):
                if i!= j:
                    pi *= Polynomial([-X[i], 1])/(X[j] - X[i])
            return pi

        P = Polynomial([])
        ## calculate sum of all lagrange polynomials
        for i in range(n):
            P += Y[i]*psi(i)

        self = P

        ## Plot
        numpts = 100

        Xg = np.linspace(min(X),max(X), numpts)

        Yg = [self[x] for x in Xg]

        plt.plot(Xg,Yg)
        plt.scatter(X, Y, c='r')
        plt.title("Interpolation using Lagrange polynomial")
        plt.xlabel("x")
        plt.ylabel("P(x)")
        plt.grid()
        plt.show()