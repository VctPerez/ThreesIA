import numpy as np

from src.costs.rukai_costs import RukaiCosts
from src.game.board.board_state import BoardState

class Node:
    # Static class variable
    cost_calculator = RukaiCosts() # Specify a cost functions calculator

    def __init__(self,father=None):
        self.father = father
        self.board = father.board.copy() if father is not None else BoardState()

        if father is None:
            # Initial state
            self.board = BoardState()
            self.board.init_board()
        else:
            self.board = father.board.copy()

        self.isObjetive = False

    def g(self):
        return self.cost_calculator.calc_g(self, self.father)

    def h(self):
        return self.cost_calculator.calc_h(self)

    def f(self):
        return self.g() + self.h()

    def get_successors(self):
        movements = ["UP", "DOWN", "RIGHT", "LEFT"]
        successors = []

        for move in movements:
            successor = Node(father=self)

            if move == "UP":
                successor.board.move_up()
            elif move == "DOWN":
                successor.board.move_down()
            elif move == "RIGHT":
                successor.board.move_right()
            elif move == "LEFT":
                successor.board.move_left()

            successor.board.insert_random_number()

            if successor.board != self.board:
                successors.append(successor)

        if not successors:
            self.isObjetive = True

        return successors
