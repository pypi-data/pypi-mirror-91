import random
import operator
import sys

# Create a class Matrix
class Matrix(object):
    
    def __init__(self, m, n, init=True):
        if init:
            self.rows = [[0]*n for x in range(m)]
        else:
            self.rows = []
        self.m = m
        self.n = n
