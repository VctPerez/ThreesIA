import pygame
from numpy.random import SeedSequence

from src.game.board.board_controller import BoardController
from src.game.board.board_state import BoardState
from src.game.board.board_view import BoardView
from src.a_star import AStar
from src.game.stats.astar_stats import AStarStats
from src.game.stats.manual_stats import ManualStats
from src.node import Node
from src.utils import config
from src.utils.config import N_ROWS, N_COLS, SEED
import numpy as np

clock = pygame.time.Clock()

class GameLogic:
    """
    Class that handles the game logic depending on the selected game mode
    """
    def __init__(self, screen, game_mode):
        """
        Initializes the game logic depending on the selected game mode
        If the game mode is 'a_star', the A* algorithm is executed and the path is stored
        If the game mode is 'manual', the initial board state is created and lets the user play
        """
        self.screen = screen
        self.game_mode = game_mode

        rng = np.random.default_rng(seed=SEED)

        if game_mode == 'a_star':
            # Initialize and run the A* algorithm
            self.astar_object = AStar(BoardState(father=None, n_rows=N_ROWS, n_cols=N_COLS, rng=rng))
            path, expanded_nodes, exec_time = self.astar_object.algorithm()
            self.path = path
            self.current_board = self.path[0] # Initial board state

            # Initialize the user interface
            self.board_view = BoardView(self.screen, board = self.current_board)
            self.stats_view = AStarStats(self.screen, expanded_nodes, exec_time, path[-1].get_board_score())

            # Initialize the time passed and the index of the path
            self.time_passed = 0
            self.index = 0
        if game_mode == 'manual':
            # Initialize the manual game mode
            self.current_board = BoardState(father=None, n_rows=N_ROWS, n_cols=N_COLS, rng=rng)

            # Initialize the user interface
            self.board_view = BoardView(self.screen, self.current_board)
            self.stats_view = ManualStats(self.screen)

            self.boardController = BoardController(self.current_board)

    def paint(self):
        """
        Handles the painting of the screen
        It calls the paint method of the board view and the stats view
        """

        # Fill the screen with a background color
        self.screen.fill("gray")

        # Render the board state and the results stats
        self.stats_view.paint()
        self.board_view.paint()

        pygame.display.flip()

    def run(self):
        """
        Runs the game loop depending on the selected game mode
        """
        if self.game_mode == 'a_star':
            self.run_a_star()
        if self.game_mode == 'manual':
            self.run_manual_control()

    def run_manual_control(self):
        """
        Game loop for the manual game mode
        It checks the user input and updates the board state
        Once the game ends, it shows the final score
        """
        run_loop = True
        check_events = True
        while run_loop:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_loop = False
                elif check_events and event.type == pygame.KEYDOWN:
                    self.boardController.handle_key_down(event.key)

            # If it is objective, show the final score
            if check_events and self.current_board.is_objective():
                self.stats_view.set_final_score(self.current_board.get_board_score())
                check_events = False # Once the game ends there is no need to check events

            self.paint()

    def run_a_star(self):
        """
        Game loop for the A* game mode
        It shows the A* algorithm statistics and the board state
        It also handles the skip button to show the final board
        """
        run_loop = True
        while run_loop:
            delta_time = clock.tick(config.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_loop = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.stats_view.handle_event(event)

            # If the skip button is pressed, show the final board
            if self.stats_view.check_skip_animation():
                self.skip_animation()
            else:
                self.update_board(delta_time)

            self.paint()

    def update_board(self, delta_time):
        """
        Update the board state according to the time passed
        The board state is updated every TIME_BETWEEN_MOVES milliseconds
        """
        self.time_passed += delta_time

        if self.game_mode == 'a_star':
            if self.index < len(self.path) and self.time_passed >= config.TIME_BETWEEN_MOVES:
                self.current_board = self.path[self.index]
                self.board_view.set_board_state(self.current_board)
                self.time_passed = 0
                self.index += 1

    def skip_animation(self):
        """
        Sets the current board to the final board state
        """
        # Just update reference once
        if self.index < len(self.path):
            self.index = len(self.path)
            self.current_board = self.path[-1]
            self.board_view.set_board_state(self.current_board)