import numpy as np

from src.strategies.heuristic.abstract_heuristic_strategy import AbstractHeuristicStrategy
import numpy

def get_manhattan_distance(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

def high_values_distances_with_corners(cells):
    # Board corners
    corner = (0,0)

    # Board max value
    max_value = numpy.max(cells)

    # Find the high values positions with the
    threshold = max_value / 2
    high_value_positions = [(i, j) for i in range(4) for j in range(4) if cells[i,j] >= threshold]

    heuristic = 0
    for (i, j) in high_value_positions:
        # Distance from the position to corner
        dist_min = min([get_manhattan_distance((i, j), corner)])
        # Add the distance to heuristic
        heuristic += dist_min

    return heuristic

def get_softness(cell1, cell2):
    """
    Calculates the softness given two cells.
    :param cell1:
    :param cell2:
    :return: softness
    """
    if cell1 == 0 or cell2 == 0:
        return 0
    elif (cell1 == 1 or cell1 == 2) and cell1 == cell2:
        return 100
    elif cell1 + cell2 == 3:
        return 0
    else:
        return abs(cell1 - cell2)

def calc_board_rows_softness(cells):
    """
    It calculates the softness iterating the rows.
    :param cells: board matrix.
    :return: the softness accumulated of the board along the rows.
    """
    softness_accumulator = 0
    for i in range(len(cells)):
        for j in range(len(cells[0])):
            if j < (len(cells[0]) - 1):
                softness_accumulator += get_softness(cells[i,j], cells[i,j+1])

    return softness_accumulator


def calc_board_cols_softness(cells):
    """
    It calculates the softness iterating the columns.
    :param cells: board matrix.
    :return: the softness accumulated of the board along the columns.
    """
    softness_acumulator = 0
    for j in range(len(cells[0])):
        for i in range(len(cells)):
            if i < (len(cells) - 1):
                softness_acumulator += get_softness(cells[i,j], cells[i+1,j])

    return softness_acumulator

def calc_board_softness(cells):
    """
    This method measures the softness of the board along the columns and rows.
    The softness of a cell will be the difference between it and its neighbour.
    :param cells: board matrix
    :return: the softness measure of the board
    """
    return calc_board_rows_softness(cells) + calc_board_cols_softness(cells)


# This heuristic values the distance from a corner to the high values, the score differnce and the softness of the board.
class HighValuesCornerHeuristic(AbstractHeuristicStrategy):
    def calc_h(self,node):
        return self._h_score_difference(node) + high_values_distances_with_corners(node.cells) + calc_board_softness(node.cells)

    def _h_score_difference(self, node):
        max_score = 64570080
        return max_score - node.get_board_score()