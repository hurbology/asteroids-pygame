import pygame
import random

from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        angle = random.uniform(20, 50)

        new_velocity_a = self.velocity.rotate(angle)
        new_velocity_b = self.velocity.rotate(-angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        new_asteroid_a = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_b = Asteroid(self.position.x, self.position.y, new_radius)

        new_asteroid_a.velocity = new_velocity_a * 1.2
        new_asteroid_b.velocity = new_velocity_b * 1.2

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        movement = self.velocity * dt
        self.position += movement