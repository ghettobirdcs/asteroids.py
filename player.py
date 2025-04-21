from circleshape import CircleShape
from shot import Shot
import constants
import pygame


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius  # pyright: ignore
        b = self.position - forward * self.radius - right  # pyright: ignore
        c = self.position - forward * self.radius + right  # pyright: ignore
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)  # pyright: ignore

    def rotate(self, dt):
        self.rotation += constants.PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * constants.PLAYER_SPEED * dt

    def shoot(self):
        if (self.timer <= 0):
            shot = Shot(self.position.x, self.position.y)  # pyright: ignore
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            shot.velocity = forward * constants.PLAYER_SHOT_SPEED
            self.timer = constants.PLAYER_SHOOT_COOLDOWN
