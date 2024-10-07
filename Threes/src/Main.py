import pygame

from src.Board import Board

def key_is_arrow_or_wasd(key):
    return (key == pygame.K_UP or key == pygame.K_DOWN or  key == pygame.K_RIGHT or key == pygame.K_LEFT
            or key == pygame.K_w or key == pygame.K_a or key == pygame.K_s or key == pygame.K_d)

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
            elif event.type == pygame.KEYDOWN and key_is_arrow_or_wasd(event.key):
                board.insert_random_number()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("gray")

    # RENDER YOUR GAME HERE
        board.paint(screen)
    # flip() the display to put your work on screen
        pygame.display.flip()
 # limits FPS to 60

pygame.quit()

