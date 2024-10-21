from src.strategies.cost.abstract_cost_strategy import AbstractCostStrategy

# Implements the cost function of the abstract class
# The cost of a movement is 1
class UnitCost(AbstractCostStrategy):

    def calc_g(self, node):
        if node.father is None:
            return 0
        else:
            return self._arc_cost() + node.father.g()

    # --------AUXILIAR FUNCTIONS--------

    def _arc_cost(self):
        return 1