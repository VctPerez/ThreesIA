import numpy
import pygame

WHITE = (255, 255, 255)

class Board:

    def __init__(self, cell_size, n_rows, n_cols, pos_x, pos_y):
        self.cell_size = cell_size
        self.cells = numpy.zeros((n_rows, n_cols))
        self.pos = (pos_x, pos_y)

    def paint(self, screen):
        for index, cell in numpy.ndenumerate(self.cells):
            cell_x = self.pos[0] + index[0] * (self.cell_size + 5)
            cell_y = self.pos[1] + index[1] * (self.cell_size + 5)
            if cell == 0:
                pygame.draw.rect(screen, WHITE, (cell_x, cell_y, self.cell_size, self.cell_size), border_radius=5)
                pygame.draw.rect(screen, (0,0,0), (cell_x, cell_y, self.cell_size, self.cell_size), 2, border_radius=5)

