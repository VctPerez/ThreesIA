import pygame
from src.utils import colors

font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 60)

class ManualStats:
    """
    Class to display the final score of the manual game mode
    """
    def __init__(self, screen):
        self.screen = screen
        self.final_score = 0

    def paint(self):
        if self.final_score == 0:
            return

        # GAME ENDED TEXT AT THE CENTER OF THE SCREEN
        game_ended_text = title_font.render("Game ended!", True, colors.BLUE)
        self.screen.blit(game_ended_text, (510, 50))

        # Render the text for points
        score_text = font.render(f"Final score: {self.final_score}", True, colors.BLACK)
        self.screen.blit(score_text, (530, 100))

    def set_final_score(self, score):
        self.final_score = score