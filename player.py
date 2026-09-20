import pygame
from circleshape import CircleShape
from constants import (
    COLOUR_PLAYER,
    FORWARD_VECTOR,
    INITIAL_PLAYER_SPEED,
    INITIAL_SHOOT_SPEED,
    INITIAL_SHOOT_COOLDOWN_SECONDS,
    LINE_WIDTH,
    MOUSE_BUTTON_1,
    PLAYER_RADIUS,
    RIGHT_ANGLE_DEGREES,
    SHIP_BASE_WIDTH_RATIO,
)
from shot import Shot

class Player(CircleShape):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0 
        self.cooldown_timer = 0

        # Player Variables
        self.speed: float = INITIAL_PLAYER_SPEED
        self.shoot_speed: float = INITIAL_SHOOT_SPEED
        self.shoot_cooldown: float = INITIAL_SHOOT_COOLDOWN_SECONDS
    
    def triangle(self) -> list[pygame.Vector2]:
        forward = FORWARD_VECTOR.rotate(self.rotation)
        perpendicular = FORWARD_VECTOR.rotate(self.rotation + RIGHT_ANGLE_DEGREES)
        half_base_width = perpendicular * (self.radius / SHIP_BASE_WIDTH_RATIO)

        tip = self.position + (forward * self.radius)
        rear_left = self.position - (forward * self.radius) - half_base_width
        rear_right = self.position - (forward * self.radius) + half_base_width
        return [tip, rear_left, rear_right]
    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, COLOUR_PLAYER, self.triangle(), LINE_WIDTH)

    def aim_at_mouse_pos(self, target_position: pygame.Vector2):
        displacement = target_position - self.position

        if displacement.length_squared() > 0:
            self.rotation = FORWARD_VECTOR.angle_to(displacement)

    def move(self, dt: float, direction: pygame.Vector2) -> None:
        if direction.length_squared() > 0:
            self.velocity = direction.normalize() * self.speed
            self.position += self.velocity * dt

    def shoot(self) -> None:
        if self.cooldown_timer > 0:
            return

        self.cooldown_timer = self.shoot_cooldown

        shot = Shot(self.position.x, self.position.y)
        direction = FORWARD_VECTOR.rotate(self.rotation)
        shot.velocity = direction * self.shoot_speed

    def handle_input(self, dt: float) -> None:
        # Aiming
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        self.aim_at_mouse_pos(mouse_pos)

        # Shooting
        if pygame.mouse.get_pressed()[MOUSE_BUTTON_1]:
            self.shoot()

        # Moving
        keys = pygame.key.get_pressed()
        move_direction = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            move_direction.y -= 1
        if keys[pygame.K_s]:
            move_direction.y += 1
        if keys[pygame.K_a]:
            move_direction.x -= 1
        if keys[pygame.K_d]:
            move_direction.x += 1

        self.move(dt, move_direction)

    def update(self, dt: float) -> None:
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt

        self.handle_input(dt)