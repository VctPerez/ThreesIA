from abc import ABC, abstractmethod


class Node(ABC):
    """
    Abstract class that represents a node in a search tree
    Defines the methods and variables that must be implemented by the superclasses
    """

    # Static variables for cost and heuristic strategies, must be implemented on inheritance
    cost_strategy = None
    heuristic_strategy = None

    def __init__(self,father=None):
        """
        Initializes the node with the father node
        :param father: father node
        """
        self.father = father
        self.isObjetive = False

    @abstractmethod
    def g(self):
        pass

    @abstractmethod
    def h(self):
        pass

    def f(self):
        """
        Calculates the total cost of the node
        :return: the sum of g and h
        """
        return self.g() + self.h()

    @abstractmethod
    def get_successors(self):
        pass
