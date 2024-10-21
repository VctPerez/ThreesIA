from src.strategies.heuristic.abstract_heuristic_strategy import AbstractHeuristicStrategy

# Implements the heuristic function of the abstract class
# This heuristic values the difference in score between the current board and the best possible board
class ScoreDifferenceHeuristic(AbstractHeuristicStrategy):

    def calc_h(self, node):
        return self._h_score_difference(node)

    # --------AUXILIAR FUNCTIONS--------

    def _h_score_difference(self, node):
        MAX_SCORE = 64570080
        return MAX_SCORE - node.get_board_score()