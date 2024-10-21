from abc import ABC, abstractmethod

# Defines the abstract class for the cost function
# All superclasses must implement the methods calc_g
class AbstractCostStrategy(ABC):
    @abstractmethod
    def calc_g(self,node):
        pass