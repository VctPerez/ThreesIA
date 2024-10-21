import numpy as np
import math

from numpy.random import BitGenerator, SeedSequence

from src.node import Node
from src.strategies.cost.merge_cost import MergeCost
from src.strategies.cost.unit_cost import UnitCost
from src.strategies.heuristic.adjacent_similar_and_large_tiles_heuristic import AdjacentSimilarAndLargeTiles
from src.strategies.heuristic.score_difference_heuristic import ScoreDifferenceHeuristic
from src.utils.config import N_COLS, N_ROWS, SEED

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
    heuristic_strategy = AdjacentSimilarAndLargeTiles()


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
            self.rng = np.random.default_rng(seed=SEED)
            self.rng.bit_generator.state = self.father.rng.bit_generator.state


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

    def get_max_tile(self):
        n = len(self.cells)
        max_value = self.cells[0][0];
        for i in range(n):
            for j in range(n):
                max_value = max(max_value, self.cells[i][j])
        return max_value

    def get_combination_quantity(self):
        n = len(self.cells)
        fusion_count = 0;
        for i in range(n):
            for j in range(n):
                current_tile = self.cells[i][j]
                if i > 0:
                    adjacent_tile = self.cells[i - 1][j]
                    if current_tile == adjacent_tile:
                        fusion_count += 1  # Cuenta como una posible fusión
                    if (current_tile == 1 and adjacent_tile == 2) or (current_tile == 2 and adjacent_tile == 1):
                        adjacent_match = True
                        fusion_count += 1  # Cuenta como una posible fusión de 1 y 2

                    # Compara con la ficha de abajo
                if i < n - 1:
                    adjacent_tile = self.cells[i + 1][j]
                    if current_tile == adjacent_tile:
                        fusion_count += 1  # Cuenta como una posible fusión
                    if (current_tile == 1 and adjacent_tile == 2) or (current_tile == 2 and adjacent_tile == 1):
                        fusion_count += 1  # Cuenta como una posible fusión de 1 y 2

                    # Compara con la ficha a la izquierda
                if j > 0:
                    adjacent_tile = self.cells[i][j - 1]
                    if current_tile == adjacent_tile:
                        fusion_count += 1  # Cuenta como una posible fusión
                    if (current_tile == 1 and adjacent_tile == 2) or (current_tile == 2 and adjacent_tile == 1):
                        fusion_count += 1  # Cuenta como una posible fusión de 1 y 2

                    # Compara con la ficha a la derecha
                if j < n - 1:
                    adjacent_tile = self.cells[i][j + 1]
                    if current_tile == adjacent_tile:
                        fusion_count += 1  # Cuenta como una posible fusión
                    if (current_tile == 1 and adjacent_tile == 2) or (current_tile == 2 and adjacent_tile == 1):
                        fusion_count += 1  # Cuenta como una posible fusión de 1 y 2
        return fusion_count

    def init_board(self):
        for i in range(7):
            self.insert_random_number()

    def copy(self):
        return BoardState(cells=np.matrix.copy(self.cells))

    def is_objective(self):
        if self.get_empty_cells() != 0:
            return False

        for (i, j), value in np.ndenumerate(self.cells):
            # Check up
            if i > 0 and check_sum(value, self.cells[i - 1, j]):
                return False
            # Check down
            if i < N_ROWS - 1 and check_sum(value, self.cells[i + 1, j]):
                return False
            # Check right
            if j < N_COLS - 1 and check_sum(value, self.cells[i, j + 1]):
                return False
            # Check left
            if j > 0 and check_sum(value, self.cells[i, j - 1]):
                return False
        return True
