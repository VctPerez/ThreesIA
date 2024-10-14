import numpy as np

# from src.main import SEED

VALUES = [1,1,1,1,2,2,2,3]

def check_sum(cell, new_cell):
    # Checks whether two cells can be merged
    return (cell + new_cell == 3 or
            (cell == new_cell and
             cell >= 3) or
            new_cell == 0)

def merge_and_replace(arr, direction):
    res = np.zeros(4)
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

    def __init__(self, father=None, n_rows=None, n_cols=None, random_generator=None):
        self.father = father

        if random_generator is None:
            self.random_generator = np.random.default_rng(father.random_generator.bit_generator)
        else:
            self.random_generator = random_generator

        if father is None:
            self.n_rows = n_rows
            self.n_cols = n_cols
            self.cells = np.zeros((n_rows, n_cols))
        else:
            self.n_rows = father.n_rows
            self.n_cols = father.n_cols
            self.cells = np.matrix.copy(father.cells)

    def getSucessors(self):
        successors = np.array()

        # MOVE UP
        successor = BoardState(self)
        successor.move_up()
        successors.append(successor)

        # MOVE DOWN
        successor = BoardState(self)
        successor.move_down()
        successors.append(successor)

        # MOVE RIGHT
        successor = BoardState(self)
        successor.move_right()
        successors.append(successor)

        # MOVE LEFT
        successor = BoardState(self)
        successor.move_left()
        successors.append(successor)

    def g(self):
        if self.father == None:
            return 0
        else:
            return 1 + self.father.g

    def h(self):
        return 0

    def f(self):
        return self.g() + self.h()

    def insert_random_number(self):
        row = self.random_generator.integers(0, 3)
        col = self.random_generator.integers(0, 3)
        print("ROW: ", row)
        print("COL: ", col)
        if self.cells[row, col] == 0:
            random_index = self.random_generator.integers(0, 7)
            self.cells[row, col] = VALUES[random_index]
        elif np.isin(0, self.cells):  # Para evitar recursion infinita en el caso de que no queden huecos libres
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
