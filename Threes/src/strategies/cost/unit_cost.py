from src.strategies.cost.abstract_cost_strategy import AbstractCostStrategy

# Implements the cost function of the abstract class
# The cost of a movement is 1
class UnitCost(AbstractCostStrategy):

    def _arc_cost(self, node):
        return 1