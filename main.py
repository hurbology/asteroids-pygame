import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state 



def main():
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}\nScreen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
    pygame.display.fill("black")
    pygame.display.flip()

if __name__ == "__main__":
    main()
