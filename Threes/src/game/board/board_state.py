import numpy as np
import math
from src.node import Node
from src.strategies.cost.unit_cost import UnitCost
from src.strategies.heuristic.score_difference_heuristic import ScoreDifferenceHeuristic
from src.utils.config import N_COLS, N_ROWS

VALUES = [1,2,3]

def check_sum(cell, new_cell):
    # Checks whether two cells can be merged
    return (cell + new_cell == 3 or
            (cell == new_cell and
             cell >= 3) or
            new_cell == 0)

def merge_and_replace(arr, direction):
    res = np.zeros(4)
    values = [i for i in arr if i != 0]
    new_values = []
    values_size = len(values)

    # if movement is to the left, it checks from left to right
    (start, stop, step) = (0,values_size-1,1) if direction == "left" else (values_size-1, 0,-1)

    #Iterate over the array and make the possible merges
    i = start
    while i * step <= stop:

        next_index = i + step
        if i*step < stop and check_sum(values[i],values[next_index]):
            # Merge and increase i so next value is skipped in the evaluation process
            new_values.append(values[i]+ values[next_index])
            i = i + step

        else:
            new_values.append(values[i])

        i = i + step

    if (values_size==1) :
        new_values = values

    if direction == "left" and len(values) > 0:
        # Set everything to the left
        res[:len(new_values)] = new_values
    if direction == "right" and len(values) > 0:
        #We have to reverse the new_values list because the values are appended left to right even thoudh we check from right to left
        new_values.reverse()
        # Set everything to the right
        res[-len(new_values):] = new_values

    return res

class BoardState(Node):
    #Static variables for cost and heuristic strategies
    cost_strategy = UnitCost()
    heuristic_strategy = ScoreDifferenceHeuristic()

    def __init__(self, father=None, n_rows=None, n_cols=None, rng=None):
        super().__init__(father)

        if father is None:
            self.n_rows = n_rows
            self.n_cols = n_cols
            self.cells = np.zeros((n_rows, n_cols))
            self.rng = rng
        else:
            self.n_rows = father.n_rows
            self.n_cols = father.n_cols
            self.cells = np.matrix.copy(father.cells)
            self.rng = np.random.default_rng(father.rng.bit_generator)

    def __eq__(self, other):
        res = (self.cells == other.cells).all()
        return res

    def get_board_score(self):
        score = 0

        for rows in self.cells:
            for cell in rows:
                if cell > 2:
                    score += np.pow(3, (1 + np.log2(cell / 3)))
        return score

    # Esto lo comento porque es demasiado y no quiero borrarlo

    # def coste_arco(self):
    #     # flat_father_cells = self.father.cells.flatten()
    #     #
    #     # father_unique_elements, father_counts = np.unique(flat_father_cells, return_counts=True)
    #     #
    #     # father_pairs_count = np.sum(father_counts // 2)
    #     #
    #     # flat_cells = self.father.cells.flatten()
    #     #
    #     # unique_elements, counts = np.unique(flat_cells, return_counts=True)
    #     #
    #     # pairs_count = np.sum(counts // 2)
    #     #
    #     # cost = 0
    #     #
    #     # if father_pairs_count > pairs_count:
    #     #     cost = father_pairs_count-pairs_count
    #     # elif father_pairs_count == pairs_count:
    #     #     cost = 1
    #     # else:
    #     #     cost = 0
    #
    #     return 1
    #
    # def g(self):
    #     if self.father is None:
    #         return 0
    #     else:
    #         return self.coste_arco() + self.father.g()
    #
    # def h_doubling_needed(self):
    #     return 16 - np.log2(self.cells.max()/3)
    #
    # def h_nmoves_for_doubling(self):
    #     N = np.log2(self.cells.max()/3)
    #     return ((np.pow(2,16))-1 + 16) -((np.pow(2,N)) - 1 + N)
    #
    # def h_biggest_number(self):
    #     max =  self.cells.max()
    #     return 98304 - max
    #
    # def h_score_difference(self):
    #     MAX_SCORE = 64570080
    #     return MAX_SCORE - self.getBoardScore()
    #
    # def h_empty_cells(self):
    #     return 16 - self.get_empty_cells()
    #
    # def h_weighted(self):
    #     return 0.50*self.h_empty_cells()+0.50*self.h_score_difference()
    #
    # def h(self):
    #     return self.h_nmoves_for_doubling()

    def g(self):
        return self.cost_strategy.calc_g(self)

    def h(self):
        return self.heuristic_strategy.calc_h(self)


    def insert_random_number(self):
        row = self.rng.integers(0, 4)
        col = self.rng.integers(0, 4)
        if self.cells[row, col] == 0:
            random_index = self.rng.integers(0, len(VALUES))
            self.cells[row, col] = VALUES[random_index]
        elif np.isin(0, self.cells):  # Para evitar recursion infinita en el caso de que no queden huecos libres
            self.insert_random_number()


    def move_up(self):
        for col in range(N_COLS):
            new_col = merge_and_replace(self.cells[:,col],direction="left")
            self.cells[:,col] = new_col

    def move_down(self):
        for col in range(N_COLS):
            new_col = merge_and_replace(self.cells[:,col],direction="right")
            self.cells[:,col] = new_col

    def move_left(self):
        for row in range(N_ROWS):
            new_row = merge_and_replace(self.cells[row,:],direction="left")
            self.cells[row,:] = new_row

    def move_right(self):
        for row in range(N_ROWS):
            new_row = merge_and_replace(self.cells[row,:],direction="right")
            self.cells[row,:] = new_row

    def get_successors(self):
        movements = ["UP", "DOWN", "RIGHT", "LEFT"]
        successors = []

        for move in movements:
            successor = BoardState(father=self)

            if move == "UP":
                successor.move_up()
            elif move == "DOWN":
                successor.move_down()
            elif move == "RIGHT":
                successor.move_right()
            elif move == "LEFT":
                successor.move_left()

            successor.insert_random_number()

            if successor != self:
                successors.append(successor)

        if not successors:
            self.isObjetive = True

        return successors

    def get_empty_cells(self):
        count = 0
        for row in range(N_ROWS):
            for col in range(N_COLS):
                if self.cells[row,col] == 0.0:
                    count = count + 1
        return count

    def init_board(self):
        for i in range(7):
            self.insert_random_number()

    def copy(self):
        return BoardState(cells=np.matrix.copy(self.cells))
