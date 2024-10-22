from src.strategies.cost.abstract_cost_strategy import AbstractCostStrategy
import numpy as np

# Implements the cost function of the abstract class
# The cost of a movement depends on the combinations made in the movement. If the number of possible combinations is greater than that of the father node,
# the cost of the moment is 3, if the number of possible combinations is equals than that of the father, the cost of the movement is 2 and if the number
# of possible combinations is less than that of the father node, the cost is 1
class MergeCost(AbstractCostStrategy):

    def _arc_cost(self, node):
        father_possible_combinations = self._node_possible_combinations(node.father)
        node_possible_combinations = self._node_possible_combinations(node)

        if father_possible_combinations > node_possible_combinations:
            cost = 1
        elif father_possible_combinations == node_possible_combinations:
            cost = 2
        else:
            cost = 3

        return cost

    # --------AUXILIAR FUNCTIONS--------

    def _node_possible_combinations(self, node):
        '''
        Computes the possible combinations of a node
        :param node: node to check for possible combinations
        :return: number of posible combinations within a given node
        '''
        flat_cells = node.cells.flatten()

        unique_elements, counts = np.unique(flat_cells, return_counts=True)

        possible_combinations = np.sum(counts // 2)

        ones = np.argwhere(node.cells == 1)
        twos = np.argwhere(node.cells == 2)

        combinations_one_and_two = len(ones) // len(twos) if len(twos) > 0 else 0

        possible_combinations += combinations_one_and_two

        return possible_combinations