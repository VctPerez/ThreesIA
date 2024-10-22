import numpy

from src.strategies.cost.abstract_cost_strategy import AbstractCostStrategy

def get_empty_cells_count(cells):
    """
    Calculates the number of empty cells.
    :param cells: Board matrix
    :return: empty cells count
    """
    count = 0
    for _, value in numpy.ndenumerate(cells):
        if value == 0:
            count += 1

    return count

# This cost is calculated accumulating the number of empty cells lost with the movements.
class EmptyCellsCost(AbstractCostStrategy):
    def calc_g(self,node):
        if node.father is None:
            return 0
        else:
            return self._arc_cost(node) + node.father.g()

    def _arc_cost(self, node):
        empty_cells_difference = get_empty_cells_count(node.father.cells) - get_empty_cells_count(node.cells)

        return empty_cells_difference if empty_cells_difference > 0 else 0