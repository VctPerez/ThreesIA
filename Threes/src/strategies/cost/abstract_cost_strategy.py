from abc import ABC, abstractmethod

class AbstractCostStrategy(ABC):
    """
    Defines the abstract class for the cost function strategy.
    All superclasses must implement the methods calc_g
    """
    def calc_g(self, node):
        if node.father is None:
            return 0
        else:
            return self._arc_cost(node) + node.father.g()

    @abstractmethod
    def _arc_cost(self, node):
        pass