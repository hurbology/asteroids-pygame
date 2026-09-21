import pygame

from logger import log_event
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
from shot import Shot
from constants import(
    COLOUR_BACKGROUND,
    FPS,
)

class Game():
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()

        self.configure_sprite_grpups()

        screen_width, screen_height = self.screen.get_size()

        self.asteroid_field = AsteroidField()
        self.player = Player(
            screen_width / 2,
            screen_height / 2,
        )

    def configure_sprite_grpups(self) -> None:
        Player.containers = (
            self.updatable, 
            self.drawable,
        )
        Asteroid.containers = (
            self.asteroids, 
            self.updatable, 
            self.drawable,
            )
        AsteroidField.containers = (self.updatable)

        Shot.containers = (
            self.shots, 
            self.updatable, 
            self.drawable
            )

    def run(self) -> None:
        while self.running:
             dt = self.clock.tick(FPS) / 1000

             self.handle_events()
             self.update(dt)
             self.handle_collisions()
             self.draw()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt: float) -> None:
        self.updatable.update(dt)

    def handle_collisions(self) -> None:
        self.handle_shot_collisions()
        self.handle_player_collisions()

    def handle_shot_collisions(self) -> None:
        for asteroid in self.asteroids:
            for shot in self.shots:
                if not asteroid.collides_with(shot):
                    continue
                log_event("asteroid_shot")
                asteroid.split()
                shot.kill()
                print("Asteroid Destroyed")
                break

    def handle_player_collisions(self) -> None:
        for asteroid in self.asteroids:
            if self.player.collides_with(asteroid):
                log_event("player_hit")
                print("Game Over!")
                self.running = False
                return

    def draw(self) -> None:
        self.screen.fill(COLOUR_BACKGROUND)

        for sprite in self.drawable:
            sprite.draw(self.screen)

        pygame.display.flip()