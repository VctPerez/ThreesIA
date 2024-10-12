import numpy
import random

VALUES = [1,1,1,1,1,2,2,3]


def check_sum(cell, new_cell):
    ''' Comprueba si se cumplen las condiciones para hacer la suma'''
    return (cell + new_cell == 3 or
            (cell == new_cell and
             cell != 2) or
            new_cell == 0)


class BoardState:

    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.cells = numpy.zeros((n_rows, n_cols))

    def insert_random_number(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if self.cells[row, col] == 0:
            random_index = random.randint(0, 7)
            self.cells[row, col] = VALUES[random_index]
        elif numpy.isin(0, self.cells):  # Para evitar recursion infinita en el caso de que no queden huecos libres
            self.insert_random_number()


    def move_up(self):
        for index, value in numpy.ndenumerate(self.cells):
            if index[1] > 0 and check_sum(self.cells[index[0], index[1]], self.cells[index[0], index[1] - 1]):
                self.cells[index[0], index[1] - 1] += value
                self.cells[index[0], index[1]] = 0

    def move_down(self):
        cells_reversed = list(numpy.ndenumerate(self.cells))
        cells_reversed.reverse()
        for index, value in cells_reversed:
            if index[1] < self.n_rows-1 and check_sum(self.cells[index[0], index[1]], self.cells[index[0], index[1] + 1]):
                self.cells[index[0], index[1] + 1] += value
                self.cells[index[0], index[1]] = 0

    def move_left(self):
        for index, value in numpy.ndenumerate(self.cells):
            if index[0] > 0 and check_sum(self.cells[index[0], index[1]], self.cells[index[0] - 1, index[1]]):
                self.cells[index[0] - 1, index[1]] += value
                self.cells[index[0], index[1]] = 0

    def move_right(self):
        cells_reversed = list(numpy.ndenumerate(self.cells))
        cells_reversed.reverse()
        for index, value in cells_reversed:
            if index[0] < self.n_cols-1 and check_sum(self.cells[index[0], index[1]], self.cells[index[0] + 1, index[1]]):
                self.cells[index[0] + 1, index[1]] += value
                self.cells[index[0], index[1]] = 0

