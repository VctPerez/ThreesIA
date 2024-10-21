from abc import ABC, abstractmethod


class Node(ABC):
    # Static variables for cost and heuristic strategies, must be implemented on inheritance
    cost_strategy = None
    heuristic_strategy = None


    def __init__(self,father=None):
        self.father = father
        self.isObjetive = False

    @abstractmethod
    def g(self):
        pass

    @abstractmethod
    def h(self):
        pass

    def f(self):
        return self.g() + self.h()

    @abstractmethod
    def get_successors(self):
        pass
