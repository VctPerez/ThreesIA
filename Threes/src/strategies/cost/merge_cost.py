from src.strategies.cost.abstract_cost_strategy import AbstractCostStrategy
import numpy as np

class MergeCost(AbstractCostStrategy):
    """
    Calculates the difference in the number of pairs of the father and the current node

    If the number of pairs in the father is greater than the number of pairs in the current node, the cost is 1
    because there has been at least a merge
    If the number of pairs in the father is equal to the number of pairs in the current node, the cost is 2
    because there has been a merge but the number of pairs has not changed
    If the number of pairs in the father is less than the number of pairs in the current node, the cost is 3
    because there has not been a merge
    """
    def _arc_cost(self, node):
        flat_father_cells = node.father.cells.flatten()

        father_unique_elements, father_counts = np.unique(flat_father_cells, return_counts=True)

        father_pairs_count = np.sum(father_counts // 2)

        flat_cells = node.cells.flatten()

        unique_elements, counts = np.unique(flat_cells, return_counts=True)

        pairs_count = np.sum(counts // 2)

        if father_pairs_count > pairs_count:
            cost = 1
        elif father_pairs_count == pairs_count:
            cost = 2
        else:
            cost = 3

        return cost