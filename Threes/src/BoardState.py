import numpy
import random
from numpy.random import random, random_integers

VALUES = [1,1,1,1,2,2,2,3,3,6]

class BoardState:

    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.cells = numpy.zeros((n_rows, n_cols))

    def insert_random_number(self):
        row = random_integers(0, 3)
        col = random_integers(0, 3)
        if self.cells[row, col] == 0:
            random_index = random_integers(0, 9)
            self.cells[row, col] = VALUES[random_index]
        elif numpy.isin(0, self.cells):  # Para evitar recursion infinita en el caso de que no queden huecos libres
            self.insert_random_number()


    def move_up(self):
        for index, value in numpy.ndenumerate(self.cells):
            if index[1] > 0 and self.check_sum(self.cells[index[0], index[1]], self.cells[index[0], index[1] - 1]):
                self.cells[index[0], index[1] - 1] += value
                self.cells[index[0], index[1]] = 0

    def move_down(self):
        for index, value in numpy.ndenumerate(self.cells):
            if index[1] < self.n_rows-1 and self.check_sum(self.cells[index[0], index[1]], self.cells[index[0], index[1] + 1]):
                self.cells[index[0], index[1] + 1] += value
                self.cells[index[0], index[1]] = 0

    def move_left(self):
        for index, value in numpy.ndenumerate(self.cells):
            if index[0] > 0 and self.check_sum(self.cells[index[0], index[1]], self.cells[index[0] - 1, index[1]]):
                self.cells[index[0] - 1, index[1]] += value
                self.cells[index[0], index[1]] = 0

    def move_right(self):
        for index, value in numpy.ndenumerate(self.cells):
            if index[0] < self.n_cols-1 and self.check_sum(self.cells[index[0], index[1]], self.cells[index[0] + 1, index[1]]):
                self.cells[index[0] + 1, index[1]] += value
                self.cells[index[0], index[1]] = 0

    def check_sum(self, cell, new_cell):
        ''' Comprueba si se cumplen las condiciones para hacer la suma'''
        return (cell == 1 and new_cell == 2 or
                cell == 2 and new_cell == 1 or
                (cell == new_cell and
                 cell != 2) or
                new_cell == 0)