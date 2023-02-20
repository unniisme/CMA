import random as rn
from Q1 import RowVectorFloat

class SquareMatrixFloat:

    def __init__(self,n, l=None):
        """
        Create a square matrix of order nxn.
        If a 2D array is passed, uses it to generate the matrix.
        """
        self.n = n
        self.list = [RowVectorFloat([0]*n) for i in range(n)]

        ## Wrapper to use in list comprehension
        def raiseDimensionError():
            raise Exception("Dimension Error")

        ## The input list should also be of dimension nxn
        if l != None:
            if len(l) == n:
                self.list = [RowVectorFloat(v) if len(v) == n else raiseDimensionError() for v in l]

    def __str__(self):
        """
        Printable form of matrix
        """

        return "The matrix is:\n" + "\n".join([str(v) for v in self.list])

    def __getitem__(self, index):
        """
        Index matrix (a[i]) to return a vector. The vector can be indexed further (a[i][j])
        """
        return self.list[index]

    def __setitem__(self, index, item):
        """
        Set entire row vector of matrix
        """
        if len(item) != self.n:
            raise Exception("Dimension error")

        self.list[index] = item

    def __mul__(self, vector):
        """
        Multiply a matrix and a rowVector
        """

        if type(vector) != RowVectorFloat:
            raise TypeError("Matrices can (for now) only be multiplied with row vectors of same length")
        if len(vector) != self.n:
            raise IndexError("Dimension mismatch")

        new = []

        for i in range(self.n):
            new.append(sum([a*b for (a,b) in zip(self[i], vector)]))

        return RowVectorFloat(new)


    def sampleSymmetric(self):
        """
        Generate a symmetric matrix where the diagonals are sampled over (0,n) and other elements are sampled over (0,1)
        """
        for i in range(self.n):
            for j in range(i):
                # Sample each element
                self[i][j] = self[j][i] = rn.random()

            # Sample diagonal
            self[i][i] = rn.random()*self.n

    def toRowEchelonForm(self):
        """
        Convert matrix to row echelon form
        """
        for i in range(self.n):
            # Convert diagonal elements to 1
            self[i] = self[i]/self[i][i]

            # Use a linear combination of the current row and the rows below to set low triangular elements to 0
            for j in range(i+1,self.n):
                self[j] = self[j] - self[i]*self[j][i]      # indices are [y][x]

    def isDRDominant(self):
        """
        Check if the matrix is diagonally row dominant
        """
        for i,row in enumerate(self):
            if row[i] < sum([x for j,x in enumerate(row.list) if i != j]):
                return False

        return True

    def jSolve(self, b, m):
        """
        Solve a linear equation Ax = b using Jacobi method.
        A is this matrix. 
        b is input. 
        x is unknown. 
        m is the number of iterations.
        """

        # error handling
        if not self.isDRDominant():
            raise Exception("Not solving because convergence is not guranteed.")


        x = [0]*self.n

        errors = []
        for iterations in range(m):
            # x_new is x(k+1), x is x(k)
            x_new = x.copy()
            for i in range(self.n):
                x_new[i] = (1/self[i][i]) * (b[i] - sum([self[i][j]*x[j] for j in range(self.n) if i!=j]))
            x = x_new
            ## Each error is Ax-b
            errors.append(abs(self*RowVectorFloat(x) - RowVectorFloat(b)))

        return (errors, x)

    
    def gsSolve(self, b, m):
        """
        Solve a linear equation Ax = b using Gauss-Siedel method.
        A is this matrix. 
        b is input. 
        x is unknown. 
        m is the number of iterations.
        """

        if not self.isDRDominant():
            raise Exception("Not solving because convergence is not guranteed.")


        x = [0]*self.n

        errors = []
        for iterations in range(m):
            # Not saving as a separate matrix. This cases the same equation to directly function as the Gauss-Siedel equation wherein the values of x[j] for j<i has already been updated in the same iteration to get the corresponding values for x(k+1)
            for i in range(self.n):
                x[i] = (1/self[i][i]) * (b[i] - sum([self[i][j]*x[j] for j in range(self.n) if i!=j]))
            errors.append(abs(self*RowVectorFloat(x) - RowVectorFloat(b)))

        return (errors, x)

    



if __name__=='__main__':

    ## Test cases

    a = SquareMatrixFloat(5)
    print(a)
    print()

    a.sampleSymmetric()
    print(a)
    a.toRowEchelonForm()
    print(a)
    print(a.isDRDominant())

    s = SquareMatrixFloat(4)
    s.sampleSymmetric()
    (e, x) = s.jSolve([1, 2, 3, 4], 10)
    print(x)
    print(e)

    s = SquareMatrixFloat(4)
    s.sampleSymmetric()
    (e, x) = s.gsSolve([1, 2, 3, 4], 10)
    print(x)
    print(e)