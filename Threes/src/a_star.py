from numpy.ma.core import empty


class AStarClass:

    def __init__(self, initial_board):
        """
        Initalize the instance in order to execute the algorithm.
        :param initial_board: the initial state
        """
        self.closed_nodes = []
        self.path = []
        self.opened_nodes = [initial_board]

    def algorithm(self):
        """A star algorithm. It searches the path with less cost."""
        while self.opened_nodes:
            # The firt opened node is moved to the closed nodes list
            current_state = self.opened_nodes[0]
            self.opened_nodes.pop(0)
            self.closed_nodes.append(current_state)

            # If this node is the objective, returns the path from initial state to objective
            if current_state.is_objective():
                self.path_to_objective(current_state)
                return self.path

            # Expand current_state successors
            successors = current_state.get_successors()
            for successor in successors:

                # If it's new, it establishes a pointer from successor to current_stat, and it is added to opened nodes
                if successor not in self.opened_nodes and successor not in self.closed_nodes:
                    successor.father = current_state
                    self.opened_nodes.append(successor)

                # If successor is not new, but it has a cost lesser than before. It redirects the pointer
                elif current_state.g() + 1 < successor.g():
                    successor.father = current_state

                    # If successor was closed, it's opened again
                    if successor in self.closed_nodes:
                        self.closed_nodes.remove(successor)
                        self.opened_nodes.append(successor)

            # When all successors have been expanded, the opened_nodes are sorted according to f() value
            self.opened_nodes.sort(key= lambda n: n.f())

        # If no objective is found, returns None
        return None

    def path_to_objective(self, state):
        """Generates the path from initial state to objective"""
        self.path.insert(0, state)
        if state.father: self.path_to_objective(state.father)