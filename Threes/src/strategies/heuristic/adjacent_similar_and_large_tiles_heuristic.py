import numpy as np

from src.strategies.heuristic.abstract_heuristic_strategy import AbstractHeuristicStrategy

# Implements the heuristic function of the abstract class
# This heuristic values the difference in score between the current board and the best possible board
class AdjacentSimilarAndLargeTiles(AbstractHeuristicStrategy):

    def calc_h(self, node):
        return self._h_adjacent_similar_large_tiles(node)

    # --------AUXILIAR FUNCTIONS--------

    def _h_adjacent_similar_large_tiles(self, node):
        MAX_SCORE = 64570080
        MAX_WHITE_SPACE = np.pow(len(node.cells),2)
        score = (MAX_SCORE + MAX_WHITE_SPACE * 2 - node.get_board_score())
        score -= node.get_empty_cells() * 2
        (is_max_on_corner, max_tile) = self.is_max_on_corner(node)
        if is_max_on_corner:
            score -= self.score_of(max_tile)

        return score

    def is_max_on_corner(self, node):
        n = len(node.cells)
        max_tile = node.get_max_tile()
        corner_positions = [(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)]
        big_in_corner = False
        for (x, y) in corner_positions:
            if node.cells[x][y] == max_tile:
                big_in_corner = True
                break
        return (big_in_corner, max_tile)

    def score_of(self, value):
        return np.pow(3, (1 + np.log2(value / 3)))


