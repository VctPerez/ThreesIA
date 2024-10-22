import pygame

class BoardController:
    """
    Class that handles the user input and updates the board state
    It is used for the manual game_mode.
    """

    def __init__(self, board_state):
        """
        Constructor of the class, it receives the board state
        :param board_state: current state of the board
        """
        self.boardState = board_state

    def handle_key_down(self, key):
        """
        Main method of the class, it receives the key pressed by the user.
        It checks if the key is an arrow or wasd key and makes the movement
        :param key: user event key
        """
        if self.key_is_arrow_or_wasd(key):
            self.make_movement(key)


    def key_is_arrow_or_wasd(self, key):
        """
        Method that checks if the key is an arrow or wasd key
        :param key: user event key
        """
        return (key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_RIGHT or key == pygame.K_LEFT
                or key == pygame.K_w or key == pygame.K_a or key == pygame.K_s or key == pygame.K_d)

    def make_movement(self, key):
        """
        Method that makes the movement of the board
        Calls the corresponding method of the board state depending on the key
        Then inserts a random number in the board
        :param key: user event key
        """
        match key:
            case pygame.K_UP | pygame.K_w:
                self.boardState.move_up()
            case pygame.K_DOWN | pygame.K_s:
                self.boardState.move_down()
            case pygame.K_LEFT | pygame.K_a:
                self.boardState.move_left()
            case pygame.K_RIGHT | pygame.K_d:
                self.boardState.move_right()
            case default:
                self.boardState.isObjetive = True
                return

        self.boardState.insert_random_number()