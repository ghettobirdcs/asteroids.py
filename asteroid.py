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
        self.points = self.polygon()

    def polygon(self):
        angle_step = (2 * math.pi) / self.num_sides
        points = []
        for i in range(self.num_sides):
            angle = i * angle_step
            x = self.position.x + math.cos(angle) * self.radius  # pyright: ignore
            y = self.position.y + math.sin(angle) * self.radius  # pyright: ignore
            points.append((x, y))  # pyright: ignore
        return points

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.polygon(), 2)

        if self.is_visible:
            for offset in self.offsets:
                new_points = [point + offset for point in self.points]
                pygame.draw.polygon(screen, "white", new_points, 2)  # pyright: ignore
        
    def update(self, dt):
        self.position += self.velocity * dt
        self.points = self.polygon()

        if not self.is_visible:
            self.is_visible = all(
                0 <= x <= constants.SCREEN_WIDTH and
                0 <= y <= constants.SCREEN_HEIGHT
                for (x, y) in self.points
            )

        if self.is_visible:
            super().update(dt)
            self.points = [
                (
                    (point[0] + self.velocity.x * dt) % constants.SCREEN_WIDTH,
                    (point[1] + self.velocity.y * dt) % constants.SCREEN_HEIGHT
                )
                for point in self.points
            ]

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
