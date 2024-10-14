import pygame
import numpy as np
import a_star as AStar
from menu import Menu

from src.boardController import BoardController
from src.boardState import BoardState
from src.boardView import Board

# Screen dimensions and other settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 100
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
fps = 60
board_x = (SCREEN_WIDTH - 4 * CELL_SIZE) // 2
board_y = (SCREEN_HEIGHT - 4 * CELL_SIZE) // 2

SEED = 1
randomGenerator = np.random.default_rng(seed=SEED)

boardState = BoardState(None, 4, 4, randomGenerator)
boardController = BoardController(boardState)
boardView = Board(100, board_x, board_y, boardState)


# Function to run the A* algorithm
def run_a_star():
    a_star_object = AStar.AStarClass(boardState)
    path = a_star_object.algorithm()
    boardView = Board(100, board_x, board_y, path[0])
    running = True
    time_passed = 0
    i = 1
    while running:
        delta_time = clock.tick(fps)
        time_passed += delta_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a background color
        screen.fill("gray")

        # Render the A* path
        if time_passed >= 500 and i < len(path):
            boardView.set_boardState(path[i])
            i += 1
            time_passed = 0

        boardView.paint(screen)
        pygame.display.flip()


# Function for manual control of the game
def run_manual_control():
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                boardController.handleKeydown(event.key)

        # Fill the screen with a background color
        screen.fill("gray")

        # Render the board state
        boardView.paint(screen)
        pygame.display.flip()


# Main entry point
if __name__ == '__main__':
    # Create menu instance
    menu = Menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Show menu and get selected option
    option = menu.show_menu()

    if option == 'a_star':
        run_a_star()
    elif option == 'manual':
        run_manual_control()

    pygame.quit()
