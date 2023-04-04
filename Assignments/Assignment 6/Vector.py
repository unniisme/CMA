import math


class RowVectorFloat:
    
    def __init__(self, l):
        """
        Create a row vector with the given list
        """
        self.list = l

    def __str__(self):
        """
        Print the vector as numbers separated by tab, and truncated appropriately
        """

        return "\t".join([str(round(i,2)) for i in self.list])

    def __len__(self):
        """
        Return dimension of vector
        """
        return len(self.list)

    def __getitem__(self, index):
        """
        Index vector (a[i])
        """
        return self.list[index]

    
    def __setitem__(self, index, item):
        """
        Use index to change an element
        """
        self.list[index] = item

    def __add__(self, other):
        """
        Add 2 vectors
        """
        ## Check if other is a vector
        if not isinstance(other, RowVectorFloat):
            raise TypeError("Vectors can only be added to vectors")

        ## Check dimension of other vector
        if len(self) != len(other):
            raise IndexError("Cannot add vectors of different dimensions")

        return RowVectorFloat([x+y for x,y in zip(self.list, other.list)])

    def __mul__(self, other):
        """
        Multiply a vector and a scalar
        """
        ## Scalars can be int or float
        if type(other) == type(self):
            raise TypeError("Cannot multiply vector with vector")

        return RowVectorFloat([other*x for x in self.list])

    def __rmul__(self, other):
        """
        Right multiply a vector and a scalar
        """
        if type(other) != int and type(other) != float:
            raise TypeError("Scalar multiplication must be with int or float")

        return RowVectorFloat([other*x for x in self.list])

    def __sub__(self, other):
        """
        Subtract 2 vectors
        """
        return self + other*(-1)

    def __truediv__(self, other):
        """
        Divide a vector by a scalar
        """
        return self * (1/other)

    def __abs__(self):
        """
        Absolute value of a vector returns it second order norm
        """
        return math.sqrt(sum([x*y for (x,y) in zip(self.list, self.list)]))

    def __tuple__(self):
        """
        Return the vector as a tuple
        """
        return tuple(self.list)

class Vector2(RowVectorFloat):

    def __init__(self, x, y):
        super().__init__([x,y])

    def x(self):
        return self[0]
    
    def y(self):
        return self[1]

if __name__ == '__main__':

    # Test cases


    a = RowVectorFloat([2,3,4])
    print(a)
    print(len(a))

    b = RowVectorFloat([])
    print(b)
    print(len(b))

    print(a[1])
    a[1] = 6
    print(a)

    try:
        sum1 = a + 3
    except Exception as e:
        print(e)


    try:
        sum1 = a + b
    except Exception as e:
        print(e)

    c = a + RowVectorFloat([1,2,-3])
    print(c)
    r1 = RowVectorFloat([1, 2 , 4])
    r2 = RowVectorFloat([1, 1 , 1])
    r3 = 2*r1 + (-3)*r2
    print(r3)
