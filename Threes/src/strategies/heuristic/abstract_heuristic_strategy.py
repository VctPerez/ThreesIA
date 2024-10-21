from abc import ABC, abstractmethod

# Defines the abstract class for the heuristic functions
# All superclasses must implement the methods calc_h
class AbstractHeuristicStrategy(ABC):

    @abstractmethod
    def calc_h(self,node):
        pass