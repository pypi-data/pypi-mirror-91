import random
import operator
import sys


class MatrixError(Exception):
    """ An exception class for Matrix """
    pass


# Create a class Matrix
class Matrix(object):
    
    def __init__(self, m, n, init=True):
        if init:
            self.rows = [[0]*n for x in range(m)]
        else:
            self.rows = []
        self.m = m
        self.n = n

    def __getitem__(self, idx):
        return self.rows[idx]
    
    def __setitem__(self, idx, item):
        self.rows[idx] = item


    def __str__(self):
        s='\n'.join([' '.join([str(item) for item in row]) for row in self.rows])
        return s + '\n'
      
     
    def getRank(self):
        return (self.m, self.n)
    
    def transpose(self):
        """ Transpose the matrix. Changes the current matrix """
        
        self.m, self.n = self.n, self.m
        self.rows = [list(item) for item in zip(*self.rows)]

        
    def getTranspose(self):
        """ Return a transpose of the matrix without
        modifying the matrix itself """
        
        m, n = self.n, self.m
        mat = Matrix(m, n)
        mat.rows =  [list(item) for item in zip(*self.rows)]
        
        return mat        

    
    def __addMat__(self, other):
        
        """ 
        Add a matrix to this matrix and
        return the new matrix. Doesn't modify
        the current matrix 
        """
        
        if self.getRank() != other.getRank():
            raise MatrixError("Trying to add matrixes of varying rank!")
        
        ret = Matrix(self.m, self.n)
        
        for x in range(self.m):
            row = [sum(item) for item in zip(self.rows[x], other[x])]
            ret[x] = row
        return ret
    
    def __subMat__(self, other):
        """ 
        Subtract a matrix from this matrix and
        return the new matrix. Doesn't modify
        the current matrix 
        """
        
        if self.getRank() != other.getRank():
            raise MatrixError("Trying to subtract matrixes of varying rank!")

        ret = Matrix(self.m, self.n)
        
        for x in range(self.m):
            row = [item[0]-item[1] for item in zip(self.rows[x], other[x])]
            ret[x] = row

        return ret
    
       
    def __mulMat__(self, other):
        """ 
        Multiple a matrix with this matrix and
        return the new matrix. Doesn't modify
        the current matrix 
        """
        
        otherm, othern = other.getRank()
        
        if (self.n != otherm):
            raise MatrixError("Matrices cannot be multiplied!")
        
        other_t = other.getTranspose()
        mul = Matrix(self.m, othern)
        
        for x in range(self.m):
            for y in range(other_t.m):
                mul[x][y] = sum([item[0]*item[1] for item in zip(self.rows[x], other_t[y])])

        return mul

   
    
    @classmethod
    def _makeMatrix(cls, rows):

        m = len(rows)
        n = len(rows[0])
        # Validity check
        if any([len(row) != n for row in rows[1:]]):
            raise MatrixError("inconsistent row length")
        mat = Matrix(m,n, init=False)
        mat.rows = rows

        return mat
    
    
    @classmethod
    def readStdin(cls):
        print('Enter matrix row by row. Type "q" to quit: ')
        rows = []
        while True:
            line = sys.stdin.readline().strip()
            if line=='q': break

            row = [int(x) for x in line.split()]
            rows.append(row)
            
        return cls._makeMatrix(rows)
    
    