import pygame

from src.utils import config
from src.menu.menu import Menu
from src.game.gameLogic import GameLogic

pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

# OPTIONS: 'a_star' or 'manual'
# SET to 'None' to show the menu
# SET to 'a_star' or 'manual' TO SKIP MENU

option = None
# option = 'a_star'
# option = 'manual'

# Main entry point
if __name__ == '__main__':

    # Show menu and get selected option
    if option is None:
        menu = Menu(screen)
        option = menu.show_menu()

    # Run the game
    game_logic = GameLogic(screen, option)
    game_logic.run()

    pygame.quit()
