from circleshape import CircleShape
import constants
import pygame
import random


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        super().draw(screen)
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        super().update(dt)
        self.position += self.velocity * dt

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
