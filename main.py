import pygame
from controllers.game_controller import GameController

def main():
    pygame.init()
    game_controller = GameController()
    game_controller.start_game()

if __name__ == '__main__':
    main()
