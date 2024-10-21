import math

from src.costs.abstract_costs import AbstractCost
from src.utils.config import N_ROWS, N_COLS

def calculate_max_score(n_cells):
    res = 0
    for i in range(n_cells):
        res += 3 * math.pow(2,i)
    return res

# Implements the cost functions of the abstract class
# The cost functions are based on the Rukai's heuristic
# NO SE SI ESTA BIEN, ESTOY A PUNTO DEL DERRAME CEREBRAL
class RukaiCosts(AbstractCost):
    max_score = calculate_max_score(N_ROWS * N_COLS)

    def calc_g(self, node, father=None):
        return self.g_unitario(father)

    def calc_h(self, node):
        return self.h_score_difference(node)

    # --------AUXILIAR FUNCTIONS--------

    def g_unitario(self,father):
        if father is None:
            return 0
        else:
            return self.coste_arco() + father.g()

    def coste_arco(self):
        return 1

    def h_score_difference(self, node):
        max_score = 64570080
        return max_score - node.board.get_board_score()