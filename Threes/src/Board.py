import numpy
import pygame
import random
from numpy.random import random, random_integers

WHITE = (255, 255, 255)
LIGHT_SALMON = (255, 160, 122)
VALUES = [1,2,3,6]
pygame.font.init()
font = pygame.font.SysFont(None, 40)  # Tamaño de fuente de 40

class Board:

    def __init__(self, cell_size, n_rows, n_cols, pos_x, pos_y):
        self.cell_size = cell_size
        self.cells = numpy.zeros((n_rows, n_cols))
        self.pos = (pos_x, pos_y)

    def paint(self, screen):
        for index, value in numpy.ndenumerate(self.cells):
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


    def insert_random_number(self):
        print(self.cells)
        row = random_integers(0,3)
        col = random_integers(0,3)
        random_index = random_integers(0,3)
        if self.cells[row, col] == 0:
            self.cells[row, col] = VALUES[random_index]
        elif numpy.isin(0, self.cells): # Para evitar recursion infinita en el caso de que no queden huecos libres
            self.insert_random_number()
