import pygame

from src.Board import Board

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CELL_SIZE = 100
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock
board_x = (SCREEN_WIDTH - 4 * CELL_SIZE) // 2
board_y = (SCREEN_HEIGHT - 4 * CELL_SIZE) // 2
board = Board(100, 4,4, board_x, board_y)


if __name__ == '__main__':
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("gray")

    # RENDER YOUR GAME HERE
        board.paint(screen)
    # flip() the display to put your work on screen
        pygame.display.flip()
 # limits FPS to 60

pygame.quit()

