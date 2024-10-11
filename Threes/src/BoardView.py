import numpy
import pygame
import random
from numpy.random import random, random_integers

from src.BoardState import BoardState

WHITE = (255, 255, 255)
LIGHT_SALMON = (255, 160, 122)
pygame.font.init()
font = pygame.font.SysFont(None, 40)  # Tamaño de fuente de 40

class Board:

    def __init__(self, cell_size, pos_x, pos_y, boardState):
        self.cell_size = cell_size
        self.pos = (pos_x, pos_y)
        self.boardState = boardState

    def paint(self, screen):
        for index, value in numpy.ndenumerate(self.boardState.cells):
            cell_x = self.pos[0] + index[0] * (self.cell_size + 5)
            cell_y = self.pos[1] + index[1] * (self.cell_size + 5)
            if value == 0:
                pygame.draw.rect(screen, WHITE, (cell_x, cell_y, self.cell_size, self.cell_size), border_radius=5)
            else:
                pygame.draw.rect(screen, LIGHT_SALMON, (cell_x, cell_y, self.cell_size, self.cell_size), border_radius=5)
                text_surface = font.render(str(int(value)), True, (0, 0, 0))  # Crear la superficie de texto
                text_rect = text_surface.get_rect(
                    center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
                screen.blit(text_surface, text_rect)

            pygame.draw.rect(screen, (0,0,0), (cell_x, cell_y, self.cell_size, self.cell_size), 2, border_radius=5)
