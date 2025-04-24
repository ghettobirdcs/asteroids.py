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
                new_points = [(x + offset[0], y + offset[1]) for (x, y) in self.points]
                pygame.draw.polygon(screen, "white", new_points, 2)
        
    def update(self, dt):
        self.position += self.velocity * dt

        for point in self.points:
            if 0 <= point[0] <= constants.SCREEN_WIDTH and 0 <= point[1] <= constants.SCREEN_HEIGHT:
                self.is_visible = True

        if self.is_visible:
            for point in self.points:
                if point[0] < 0:
                    self.position.x += constants.SCREEN_WIDTH
                elif point[0] > constants.SCREEN_WIDTH:
                    self.position.x -= constants.SCREEN_WIDTH
                if point[1] < 0:
                    self.position.y += constants.SCREEN_HEIGHT
                elif point[1] > constants.SCREEN_HEIGHT:
                    self.position.y -= constants.SCREEN_HEIGHT

        self.points = self.polygon()
        
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
