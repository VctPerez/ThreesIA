import pygame
import numpy as np

from src.boardController import BoardController
from src.boardState import BoardState
from src.boardView import Board


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 100
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock
board_x = (SCREEN_WIDTH - 4 * CELL_SIZE) // 2
board_y = (SCREEN_HEIGHT - 4 * CELL_SIZE) // 2

SEED = 1
randomGenerator = np.random.default_rng(seed=SEED)

boardState = BoardState(None,4, 4, randomGenerator)
boardView = Board(100, board_x, board_y, boardState)
boardController = BoardController(boardState)

if __name__ == '__main__':
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                boardController.handleKeydown(event.key)

        # fill the screen with a color to wipe away anything from last frame

        screen.fill("gray")

    # RENDER YOUR GAME HERE
        boardView.paint(screen)
    # flip() the display to put your work on screen
        pygame.display.flip()
 # limits FPS to 60

pygame.quit()

