import numpy
import pygame

from src.utils import colors
from src.utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE

pygame.font.init()
font = pygame.font.SysFont(None, 40)  # Tamaño de fuente de 40

board_x = (SCREEN_WIDTH - 4 * CELL_SIZE) // 2
board_y = (SCREEN_HEIGHT - 4 * CELL_SIZE) // 2

def choose_color(value):
    if value < 3:
        return colors.BEIGE
    elif value < 12:
        return colors.YELLOW
    elif value < 33:
        return colors.ORANGE
    elif value < 69:
        return colors.RED
    else:
        return colors.GOLD

class Board:

    def __init__(self, screen, board):
        self.screen = screen
        self.pos = (board_x, board_y)
        self.boardState = board

    def paint(self):
        for index, value in numpy.ndenumerate(self.boardState.cells):
            cell_x = self.pos[0] + index[1] * (CELL_SIZE + 5)
            cell_y = self.pos[1] + index[0] * (CELL_SIZE + 5)
            if value == 0:
                pygame.draw.rect(self.screen, colors.WHITE, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), border_radius=5)
            else:
                pygame.draw.rect(self.screen, choose_color(value), (cell_x, cell_y, CELL_SIZE, CELL_SIZE), border_radius=5)
                text_surface = font.render(str(int(value)), True, (0, 0, 0))  # Crear la superficie de texto
                text_rect = text_surface.get_rect(
                    center=(cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2))
                self.screen.blit(text_surface, text_rect)

            pygame.draw.rect(self.screen, (0,0,0), (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 2, border_radius=5)


    def set_boardState(self, new_board):
        self.boardState = new_board