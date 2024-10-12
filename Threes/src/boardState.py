import numpy
import random

VALUES = [1,1,1,1,1,2,2,3]

def check_sum(cell, new_cell):
    # Checks whether two cells can be merged
    return (cell + new_cell == 3 or
            (cell == new_cell and
             cell >= 3) or
            new_cell == 0)

def merge_and_replace(arr, direction):
    res = numpy.zeros(4)
    values = [i for i in arr if i != 0]
    values_size = len(values)

    # if movement is to the left, it checks from left to right
    (start, stop, step) = (0,values_size-1,1) if direction == "left" else (values_size-1, 0,-1)
    
    if values_size > 1:
        #Iterate over the array and check if one merge is possible
        for i in range(start,stop,step):
            next_index = i+1 if direction == "left" else i-1
            if check_sum(values[i],values[next_index]):
                # Merge and remove the next value
                values[i] = values[i]+ values[next_index]
                values.pop(next_index)
                # Only one merge per movement
                break

    if direction == "left" and len(values) > 0:
        # Set everything to the left
        res[:len(values)] = values
    if direction == "right" and len(values) > 0:
        # Set everything to the right
        res[-len(values):] = values

    return res

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
        for col in range(self.n_cols):
            new_col = merge_and_replace(self.cells[:,col],direction="left")
            self.cells[:,col] = new_col

    def move_down(self):
        for col in range(self.n_cols):
            new_col = merge_and_replace(self.cells[:,col],direction="right")
            self.cells[:,col] = new_col

    def move_left(self):
        for row in range(self.n_rows):
            new_row = merge_and_replace(self.cells[row,:],direction="left")
            self.cells[row,:] = new_row

    def move_right(self):
        for row in range(self.n_rows):
            new_row = merge_and_replace(self.cells[row,:],direction="right")
            self.cells[row,:] = new_row
