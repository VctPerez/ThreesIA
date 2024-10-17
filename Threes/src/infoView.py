import pygame
import colors

font = pygame.font.Font(None, 40)

class InfoView:
    def __init__(self, screen, n_expanded_nodes, exec_time):
        self.screen = screen
        self.n_expanded_nodes = n_expanded_nodes
        self.exec_time = exec_time
        self.skip_button = pygame.Rect(30, 250, 250, 45)
        self.skip_animation = False

    def paint(self):
        # Render the text for expanded nodes
        nodes_text = font.render(f"Expanded Nodes: {self.n_expanded_nodes}", True, colors.BLACK)
        # Render the text for execution time
        time_text = font.render(f"Execution Time: {self.exec_time:.2f} s", True, colors.BLACK)

        # Draw the skip button
        pygame.draw.rect(self.screen, colors.CYAN, self.skip_button)
        skip_text = font.render("Show final board", True, colors.BLACK)

        # Blit the text onto the screen at the top-left corner
        self.screen.blit(nodes_text, (30, 30))
        self.screen.blit(time_text, (30, 100))
        self.screen.blit(skip_text, (40, 260))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.skip_button.collidepoint(event.pos):
                self.skip_animation = True

    def check_skip_animation(self):
        return self.skip_animation