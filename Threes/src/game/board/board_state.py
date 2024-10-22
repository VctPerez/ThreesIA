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
             cell >= 3))

def merge_and_replace(arr, direction):
    """
    This function checks the values of the array and merges them in the specified direction
    :param arr: Row or column of the board.
    :param direction: "left" or "right". The movement determines the direction to iterate over the array for merge checks.
    :return: The array with the possible merges and filled with zeros on the empty spaces.
    """

    res = np.zeros(4)
    values = [i for i in arr if i != 0]
    new_values = []
    values_size = len(values)

    # The movement determines the direction to iterate over the array.
    # if movement is to the left, it checks from left to right
    (start, stop, step) = (0,values_size-1,1) if direction == "left" else (values_size-1, 0,-1)

    # Iterate over the array and make the possible merges
    # Fill the new_values list with the merged values
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

    # If there is only one value in the array, there cannot be any merge
    if values_size==1:
        new_values = values

    # Fill the res array with the new_values list
    if direction == "left" and len(values) > 0:
        # Set values to the left of the res array. Leaving the rest of the array with zeros
        res[:len(new_values)] = new_values
    if direction == "right" and len(values) > 0:
        # We have to reverse the new_values list because the values are appended left to right even thoudh we check from right to left
        new_values.reverse()
        # Set values to the right of the res array. Leaving the rest of the array with zeros
        res[-len(new_values):] = new_values

    return res

class BoardState(Node):
    """
    Class that defines the state of the board.
    It inherits from Node class and implements the methods to calculate the costs and get the successors.
    Contains all logic related to the board state and the game rules.
    """
    #Static variables for cost and heuristic strategies
    cost_strategy = UnitCost()
    heuristic_strategy = AdjacentSimilarAndLargeTiles()


    def __init__(self, father=None, n_rows=None, n_cols=None, rng=None):
        """
        Class constructor, initializes the board state.
        If it has no father, it means it is the root node, so it initializes the board with random numbers.
        Otherwise, it copies the father's board state and the random number generator.
        :param father: father node
        :param n_rows: number of rows
        :param n_cols: number of columns
        :param rng: random number generator. It is passed in order to copy its state when creating a new node.
        """
        super().__init__(father)

        if father is None:
            self.n_rows = n_rows
            self.n_cols = n_cols
            self.cells = np.zeros((n_rows, n_cols))
            self.rng = rng
            self.init_board()
        else:
            self.n_rows = father.n_rows
            self.n_cols = father.n_cols
            self.cells = np.matrix.copy(father.cells)
            self.rng = np.random.default_rng(seed=SEED)
            # Copy the state so that the random number generator is the same
            self.rng.bit_generator.state = self.father.rng.bit_generator.state


    def __eq__(self, other):
        res = (self.cells == other.cells).all()
        return res

    def get_board_score(self):
        """
        Applies the score function to every cell in the board.
        :return: sum of the scores of all the cells in the board.
        """
        score = 0

        for rows in self.cells:
            for cell in rows:
                if cell > 2:
                    score += np.pow(3, (1 + np.log2(cell / 3)))
        return score

    def g(self):
        """
        Implementation of the cost function.
        It calls a strategy to calculate the cost of the current state.
        :return: cost g of the current state.
        """
        return self.cost_strategy.calc_g(self)

    def h(self):
        """
        Implementation of the heuristic function.
        It calls a strategy to calculate the heuristic of the current state.
        :return: cost h of the current state.
        """
        return self.heuristic_strategy.calc_h(self)


    def insert_random_number(self):
        """
        Inserts a random number in a random empty cell of the board.
        The number is chosen from the VALUES array.
        """
        row = self.rng.integers(0, 4)
        col = self.rng.integers(0, 4)
        if self.cells[row, col] == 0:
            random_index = self.rng.integers(0, len(VALUES))
            self.cells[row, col] = VALUES[random_index]
        # If the random cell is occupied, it tries again
        # But first it checks whether the board is full
        elif np.isin(0, self.cells):
            self.insert_random_number()


    def move_up(self):
        """
        It applies the move_up rule. It checks every possible merge
        """
        # For each column in the array
        for col in range(N_COLS):
            # Get the column and apply the merges from top to bottom
            new_col = merge_and_replace(self.cells[:,col],direction="left")
            # Replace the column with the new values
            self.cells[:,col] = new_col

    def move_down(self):
        """
        It applies the move_down rule. It checks every possible merge
        """
        # For each column in the array
        for col in range(N_COLS):
            # Get the column and apply the merges from bottom to top
            new_col = merge_and_replace(self.cells[:,col],direction="right")
            # Replace the column with the new values
            self.cells[:,col] = new_col

    def move_left(self):
        """
        It applies the move_left rule. It checks every possible merge
        """
        # For each row in the array
        for row in range(N_ROWS):
            # Get the row and apply the merges from left to right
            new_row = merge_and_replace(self.cells[row,:],direction="left")
            # Replace the row with the new values
            self.cells[row,:] = new_row

    def move_right(self):
        """
        It applies the move_right rule. It checks every possible merge
        """
        # For each row in the array
        for row in range(N_ROWS):
            # Get the row and apply the merges from right to left
            new_row = merge_and_replace(self.cells[row,:],direction="right")
            # Replace the row with the new values
            self.cells[row,:] = new_row

    def get_successors(self):
        """
        It generates the successors of the current state. It applies the four movements rules to the current state.
        :return: list of successor nodes.
        """
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

            # If the successor is different from the current state, it means the movement was valid
            if successor != self:
                # Because of rng, all successors insert the same number at the same position, if possible
                successor.insert_random_number()
                successors.append(successor)

        # If there are no successors, it means the game is over
        if not successors:
            self.isObjetive = True

        return successors

    def get_empty_cells(self):
        """
        Auxiliary function to get the number of empty cells in the board.
        :return: amount of empty cells
        """
        count = 0
        for row in range(N_ROWS):
            for col in range(N_COLS):
                if self.cells[row,col] == 0.0:
                    count = count + 1
        return count

    def get_max_tile(self):
        """
        Auxiliary function to get the maximum value in the board.
        :return: max value in the board
        """
        return np.max(self.cells)

    def get_merges_quantity(self):
        """
        Calculates the amount of possible merges in the board.
        :return: sum of the possible merges
        """
        merges_count = 0

        for (i, j), value in np.ndenumerate(self.cells):
            # Check up
            if i > 0 and check_sum(value, self.cells[i - 1, j]):
                merges_count += 1
            # Check down
            if i < N_ROWS - 1 and check_sum(value, self.cells[i + 1, j]):
                merges_count += 1
            # Check right
            if j < N_COLS - 1 and check_sum(value, self.cells[i, j + 1]):
                merges_count += 1
            # Check left
            if j > 0 and check_sum(value, self.cells[i, j - 1]):
                merges_count += 1

        return merges_count

    def init_board(self):
        """
        Initializes the board with 7 random numbers.
        """
        for i in range(7):
            self.insert_random_number()

    def is_objective(self):
        """
        Used for the manual game_mode. It checks whether the game is over.
        If there are no empty cells and no possible merges, the game is over.
        :return: true if the game is over, false otherwise.
        """
        return self.get_empty_cells() == 0 and self.get_merges_quantity() == 0
