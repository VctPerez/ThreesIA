import pygame

font = pygame.font.Font(None, 40)

class InfoView:
    def __init__(self, screen, n_expanded_nodes, exec_time):
        self.screen = screen
        self.n_expanded_nodes = n_expanded_nodes
        self.exec_time = exec_time

    def paint(self):
        # Render the text for expanded nodes
        nodes_text = font.render(f"Expanded Nodes: {self.n_expanded_nodes}", True, (0, 0, 0))
        # Render the text for execution time
        time_text = font.render(f"Execution Time: {self.exec_time:.2f} s", True, (0, 0, 0))

        # Blit the text onto the screen at the top-left corner
        self.screen.blit(nodes_text, (30, 30))
        self.screen.blit(time_text, (30, 100))
