import numpy as np
import pygame

from src.game.board.boardController import BoardController
from src.game.board.boardState import BoardState
from src.game.board.boardView import Board
from src.a_star import AStarClass
from src.game.stats.infoView import InfoView
from src.utils import config

SEED = 2
randomGenerator = np.random.default_rng(seed=SEED)

clock = pygame.time.Clock()

class GameLogic:
    def __init__(self, screen, game_mode):
        self.screen = screen
        self.game_mode = game_mode
        self.boardState = BoardState(None, config.N_ROWS, config.N_COLS, randomGenerator)
        self.boardController = BoardController(self.boardState)

        if game_mode == 'a_star':
            # Initialize the A* algorithm
            self.a_star_object = AStarClass(self.boardState)

            a_star_info = self.a_star_object.algorithm()

            self.path = a_star_info[0]
            self.boardView = Board(self.screen, board = self.path[0])
            self.infoView = InfoView(self.screen, a_star_info[1], a_star_info[2])

            # Initialize the time passed and the index of the path
            self.time_passed = 0
            self.index = 0

        if game_mode == 'manual':
            self.boardView = Board(self.screen, self.boardState)

    def paint(self):
        # Fill the screen with a background color
        self.screen.fill("gray")

        # Render the board state and the results stats
        if self.game_mode == 'a_star':
            self.infoView.paint()

        self.boardView.paint()

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
            delta_time = clock.tick(config.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_loop = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.infoView.handle_event(event)

            if self.infoView.check_skip_animation():
                self.skip_animation()
            else:
                self.update_board(delta_time)

            self.paint()

    def update_board(self, delta_time):
        self.time_passed += delta_time

        if self.game_mode == 'a_star':
            if self.index < len(self.path) and self.time_passed >= config.TIME_BETWEEN_MOVES:
                self.boardState = self.path[self.index]
                self.boardView.set_boardState(self.boardState)
                self.time_passed = 0
                self.index += 1

    def skip_animation(self):
        # Just update reference once
        if self.index < len(self.path):
            self.index = len(self.path)
            self.boardState = self.path[-1]
            self.boardView.set_boardState(self.boardState)