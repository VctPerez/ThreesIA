import pygame

from src.utils.colors import WHITE, GRAY, BLUE, GREEN, ORANGE
from src.utils.config import SCREEN_WIDTH, SCREEN_HEIGHT

# Class to handle the main menu
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 60)  # Font for the title

    # Function to draw buttons with rounded corners
    def draw_rounded_button(self, text, color, x, y, width, height, border_radius):
        pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=border_radius)
        text_surface = self.font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)

    # Function to draw the game title at the top of the screen
    def draw_title(self, title, color, x, y, width, height):
        pygame.draw.rect(self.screen, color, (x, y, width, height))  # Draw the rectangle for the title
        title_surface = self.title_font.render(title, True, WHITE)
        title_rect = title_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(title_surface, title_rect)  # Draw the title text inside the rectangle

    # Function to handle menu display and interaction
    def show_menu(self):
        running = True

        while running:
            self.screen.fill(GRAY)

            # Draw the title at the top of the screen
            self.draw_title("Threes Game", ORANGE, SCREEN_WIDTH // 2 - 300, 50, 600, 100)

            # Draw the buttons with rounded corners
            self.draw_rounded_button("Run A*", BLUE, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 100, 20)
            self.draw_rounded_button("Manual", GREEN, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 100, 20)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    # Check if the click is within the A* button
                    if SCREEN_WIDTH // 2 - 150 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 150 and SCREEN_HEIGHT // 2 - 50 <= \
                            mouse_pos[1] <= SCREEN_HEIGHT // 2 + 50:
                        return 'a_star'
                    # Check if the click is within the Manual Control button
                    elif SCREEN_WIDTH // 2 - 150 <= mouse_pos[
                        0] <= SCREEN_WIDTH // 2 + 150 and SCREEN_HEIGHT // 2 + 100 <= mouse_pos[
                        1] <= SCREEN_HEIGHT // 2 + 200:
                        return 'manual'

        return None
