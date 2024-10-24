import numpy as np
import time

from src.utils.config import SEED
randomGenerator = np.random.default_rng(SEED)


def print_node(node):
    print("------------------")
    print(node.cells)
    print("Coste (g) =", node.g())
    print("Heuristica (h) =", node.h())
    print("Valor del nodo (f) =", node.f())

def print_path(path):
    print("\n\n\n-----------PATH-----------\n\n\n")
    for node in path:
        print_node(node)


class AStar:

    def __init__(self, initial_board):
        """
        Initalize the instance in order to execute the algorithm.
        :param initial_board: the initial state
        """
        self.closed_nodes = []
        self.path = []
        self.opened_nodes = [initial_board]

    def algorithm(self):
        start_time = time.time()
        """A star algorithm. It searches the path with less cost."""
        while self.opened_nodes:
            # The firt opened node is moved to the closed nodes list
            current_node = self.opened_nodes[0]
            self.opened_nodes.pop(0)
            self.closed_nodes.append(current_node)

            # Expand current_state successors
            successors = current_node.get_successors()

            # If this node is the objective, returns the path from initial state to objective
            if current_node.isObjetive:
                self.path_to_objective(current_node)
                print_path(self.path)
                finish_time = time.time()

                # Return the path, number of explored nodes and execution time
                return self.path, len(self.closed_nodes), finish_time - start_time

            for successor in successors:
                print_node(successor)

                # If it's new, it establishes a pointer from successor to current_stat, and it is added to opened nodes
                if successor not in self.opened_nodes and successor not in self.closed_nodes:
                    successor.father = current_node
                    self.opened_nodes.append(successor)

                # If successor is not new, but it has a cost lesser than before. It redirects the pointer
                elif current_node.g() + 1 < successor.g():
                    successor.father = current_node

                    # If successor was closed, it's opened again
                    if successor in self.closed_nodes:
                        self.closed_nodes.remove(successor)
                        self.opened_nodes.append(successor)

            # When all successors have been expanded, the opened_nodes are sorted according to f() value
            self.opened_nodes.sort(key=lambda n: n.f())
            # self.opened_nodes.reverse()

        finish_time = time.time()
        # If no objective is found, returns None
        return None, len(self.closed_nodes), finish_time - start_time

    def path_to_objective(self, node):
        """Generates the path from initial state to objective"""
        self.path.insert(0, node)
        if node.father: self.path_to_objective(node.father)


# if __name__ == '__main__':
#     aStar = AStar(boardState)
#     path = aStar.algorithm()
#     if path:
#         for elem in (path):
#             print("--------------------------------------")
#             print(elem.cells)
