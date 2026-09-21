import pygame

from circleshape import CircleShape
from constants import(
    SHOT_RADIUS,
    SHOT_LIFETIME,
    LINE_WIDTH,
)

class Shot(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)
        self.remaining_lifetime = SHOT_LIFETIME

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius)

    def update(self, dt: float) -> None:
        movement = self.velocity * dt
        self.position += movement
        self.remaining_lifetime -= dt
        if self.remaining_lifetime <= 0:
            self.kill()