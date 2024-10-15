import pygame
from numpy.f2py.f90mod_rules import options

import config
from menu import Menu
from gameLogic import GameLogic

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

    game_logic = GameLogic(screen, option)
    game_logic.run()

    pygame.quit()
