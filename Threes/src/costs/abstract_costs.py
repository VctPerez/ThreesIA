from abc import ABC, abstractmethod

# Defines the abstract class for the cost functions
# All superclasses must implement the methods calc_g and calc_h
class AbstractCost(ABC):
    @abstractmethod
    def calc_g(self,node, father=None):
        pass

    @abstractmethod
    def calc_h(self,node):
        pass