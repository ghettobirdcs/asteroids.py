from circleshape import CircleShape
from shot import Shot
import constants
import pygame


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.acceleration = 0

    def triangle(self, offset):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius + offset  # pyright: ignore
        b = self.position - forward * self.radius + offset - right  # pyright: ignore
        c = self.position - forward * self.radius + offset + right  # pyright: ignore
        return [a, b, c]

    def draw(self, screen):
        for offset in self.offsets:
            pygame.draw.polygon(screen, "white", self.triangle(offset), 2)  # pyright: ignore

    def rotate(self, dt):
        self.rotation += constants.PLAYER_TURN_SPEED * dt

    def update(self, dt):
        super().update(dt)
        self.timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt, True)
        if keys[pygame.K_s]:
            self.move(-dt, True)
        if keys[pygame.K_SPACE]:
            self.shoot()
        # Decelerate the player when not pressing 'w' or 's' to move
        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.move(dt, False)

    def move(self, dt, accelerating=False):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        if (accelerating and dt > 0):
            self.acceleration = constants.PLAYER_ACCELERATION
            self.velocity += forward * self.acceleration * dt
        elif (accelerating and dt < 0):
            self.acceleration = -constants.PLAYER_ACCELERATION
            self.velocity -= forward * self.acceleration * dt
        else:
            self.acceleration = 0

        self.velocity *= 0.993

        if self.velocity.length() > constants.PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(constants.PLAYER_MAX_SPEED)

        self.position += self.velocity

    def shoot(self):
        if (self.timer <= 0):
            shot = Shot(self.position.x, self.position.y)  # pyright: ignore
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            shot.velocity = forward * constants.PLAYER_SHOT_SPEED
            self.timer = constants.PLAYER_SHOOT_COOLDOWN
