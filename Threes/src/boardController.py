import pygame

class BoardController:

    def __init__(self, boardState):
        self.boardState = boardState

    def handleKeydown(self, key):
        if self.key_is_arrow_or_wasd(key):
            self.make_movement(key)

            print(self.boardState.cells)

    def key_is_arrow_or_wasd(self, key):
        return (key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_RIGHT or key == pygame.K_LEFT
                or key == pygame.K_w or key == pygame.K_a or key == pygame.K_s or key == pygame.K_d)

    def make_movement(self, key):
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