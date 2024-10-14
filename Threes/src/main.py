import pygame
import numpy as np
import a_star as AStar

from src.boardController import BoardController
from src.boardState import BoardState
from src.boardView import Board


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 100
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
time_passed = 0
fps = 60
board_x = (SCREEN_WIDTH - 4 * CELL_SIZE) // 2
board_y = (SCREEN_HEIGHT - 4 * CELL_SIZE) // 2

SEED = 1
randomGenerator = np.random.default_rng(seed=SEED)

boardState = BoardState(None,4, 4, randomGenerator)
boardController = BoardController(boardState)

a_star_object = AStar.AStarClass(boardState)
path = a_star_object.algorithm()
boardView = Board(100, board_x, board_y, path[0])

if __name__ == '__main__':
    running = True
    i = 1
    while running:
        delta_time = clock.tick(fps)
        time_passed += delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                boardController.handleKeydown(event.key)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("gray")

    # RENDER YOUR GAME HERE
        if time_passed >= 500 and i < len(path):
            boardView.set_boardState(path[i])
            # print(path[i].cells)
            i += 1
            time_passed = 0

        boardView.paint(screen)
    # flip() the display to put your work on screen
        pygame.display.flip()

 # limits FPS to 60

pygame.quit()

