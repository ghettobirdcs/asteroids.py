from circleshape import CircleShape
import constants
import pygame
import random
import math


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.is_visible = False
        self.num_sides = random.randint(5, 7)
        self.uniform = random.uniform(0.8, 1.2)
        # FIXME: jitter not working properly - currently unimplemented
        self.jitter = pygame.Vector2(
            random.uniform(-0.5 * self.radius, 0.5 * self.radius),
            random.uniform(-0.5 * self.radius, 0.5 * self.radius)
        )
        self.points = self.polygon()

    def polygon(self, offset=pygame.Vector2(0, 0)):
        angle_step = (2 * math.pi) / self.num_sides
        points = []
        for i in range(self.num_sides):
            angle = i * angle_step
            random_radius = self.radius * self.uniform
            # Use Vector2 for all calculations
            vertex = self.position + pygame.Vector2(math.cos(angle), math.sin(angle)) * random_radius + offset  # pyright: ignore
            points.append((vertex.x, vertex.y))
        return points

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.polygon(), 2)

        if self.is_visible:
            for offset in self.offsets:
                pygame.draw.polygon(screen, "white", self.polygon(offset), 2)  # pyright: ignore
        
    def update(self, dt):
        self.position += self.velocity * dt
        self.points = self.polygon(self.velocity * dt)

        if not self.is_visible:
            self.is_visible = all(
                0 <= x <= constants.SCREEN_WIDTH and
                0 <= y <= constants.SCREEN_HEIGHT
                for (x, y) in self.points
            )

        if self.is_visible:
            super().update(dt)

    def split(self):
        self.kill()
        if (self.radius <= constants.ASTEROID_MIN_RADIUS):
            return
        else:
            # Spawn 2 more asteroids
            rand_angle = random.uniform(20, 50)

            new_vectors = [
                self.velocity.rotate(-rand_angle),
                self.velocity.rotate(rand_angle)
            ]
            new_radius = self.radius - constants.ASTEROID_MIN_RADIUS

            for vector in new_vectors:
                asteroid = Asteroid(self.position.x, self.position.y, new_radius)  # pyright: ignore
                asteroid.velocity = vector * 1.2
