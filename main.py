import pygame

from game import Game
from constants import(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)



def main():
    pygame.init()

    try:
        screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        game = Game(screen)
        game.run()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
