from numpy.ma.core import empty


class A_star_class:

    def __init__(self, initial_board):
        self.closed_nodes = []
        self.opened_nodes = [initial_board]

    def g(self, state):
        return 1

    def h(self, state):
        return 1

    def f(self, state):
        return self.g(state) + self.h(state)

    def algorithm(self):
        while self.opened_nodes:
            current_state = self.opened_nodes[0]
            self.opened_nodes.pop(0)
            self.closed_nodes.append(current_state)
    
        return None
