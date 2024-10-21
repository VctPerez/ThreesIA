from src.strategies.cost.abstract_cost_strategy import AbstractCostStrategy
import numpy as np

# Implements the cost function of the abstract class
# The cost of a movement is 1
class MergeCost(AbstractCostStrategy):

    def _arc_cost(self, node):
        flat_father_cells = node.father.cells.flatten()

        father_unique_elements, father_counts = np.unique(flat_father_cells, return_counts=True)

        father_pairs_count = np.sum(father_counts // 2)

        flat_cells = node.father.cells.flatten()

        unique_elements, counts = np.unique(flat_cells, return_counts=True)

        pairs_count = np.sum(counts // 2)

        cost = 0

        if father_pairs_count > pairs_count:
            cost = father_pairs_count-pairs_count
        elif father_pairs_count == pairs_count:
            cost = 1
        else:
            cost = 0

        return cost