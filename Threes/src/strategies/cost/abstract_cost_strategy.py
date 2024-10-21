from abc import ABC, abstractmethod

# Defines the abstract class for the cost function
# All superclasses must implement the methods calc_g
class AbstractCostStrategy(ABC):

    def calc_g(self, node):
        if node.father is None:
            return 0
        else:
            return self._arc_cost(node) + node.father.g()

    @abstractmethod
    def _arc_cost(self, node):
        pass