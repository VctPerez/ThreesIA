import numpy as np
import pygame

from src.boardController import BoardController
from src.boardState import BoardState
from src.boardView import Board
from a_star import AStarClass
import config

SEED = 1
randomGenerator = np.random.default_rng(seed=SEED)

clock = pygame.time.Clock()

class GameLogic:
    def __init__(self, screen, game_mode):
        self.screen = screen
        self.game_mode = game_mode
        self.boardState = BoardState(None,config.N_ROWS, config.N_COLS, randomGenerator)
        self.boardController = BoardController(self.boardState)
        if game_mode == 'a_star':
            # Initialize the A* algorithm
            self.a_star_object = AStarClass(self.boardState)
            self.path = self.a_star_object.algorithm()
            self.boardView = Board(100, self.path[0])

            # Initialize the time passed and the index of the path
            self.time_passed = 0
            self.index = 0
        else:
            self.boardView = Board(100, self.boardState)

    def update_board(self, delta_time):
        self.time_passed += delta_time

        if self.game_mode == 'a_star':
            if self.index < len(self.path) and self.time_passed >= config.TIME_BETWEEN_MOVES:
                self.boardState = self.path[self.index]
                self.boardView.set_boardState(self.boardState)
                self.time_passed = 0
                self.index += 1

    def paint(self):
        # Fill the screen with a background color
        self.screen.fill("gray")
        # Render the board state
        self.boardView.paint(self.screen)
        pygame.display.flip()

    def run(self):
        if self.game_mode == 'a_star':
            self.run_a_star()
        if self.game_mode == 'manual':
            self.run_manual_control()

    def run_manual_control(self):
        run_loop = True
        while run_loop:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_loop = False
                elif event.type == pygame.KEYDOWN:
                    self.boardController.handleKeydown(event.key)

            self.paint()

    def run_a_star(self):
        run_loop = True
        while run_loop:
            delta_time = clock.tick(SEED)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_loop = False

            self.update_board(delta_time)
            self.paint()