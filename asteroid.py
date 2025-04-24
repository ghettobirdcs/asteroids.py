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
        translated = [(self.position.x + x, self.position.y + y) for (x, y) in self.points]  # pyright: ignore
        pygame.draw.polygon(screen, "white", translated, 2)

        if self.is_visible:
            for offset in self.offsets:
                new_points = [(x + offset[0], y + offset[1]) for (x, y) in self.points]
                pygame.draw.polygon(screen, "white", new_points, 2)
        
    def update(self, dt):
        self.is_visible = any(
            self.radius <= x <= constants.SCREEN_WIDTH - self.radius and self.radius <= y <= constants.SCREEN_HEIGHT - self.radius
            for (x, y) in self.points
        )

        if self.is_visible:
            # Wrap around horizontally and vertically for each vertex
            for i, (x, y) in enumerate(self.points):
                if x < 0:
                    self.points[i] = (x + constants.SCREEN_WIDTH, y)
                elif x > constants.SCREEN_WIDTH:
                    self.points[i] = (x - constants.SCREEN_WIDTH, y)

                if y < 0:
                    self.points[i] = (x, y + constants.SCREEN_HEIGHT)
                elif y > constants.SCREEN_HEIGHT:
                    self.points[i] = (x, y - constants.SCREEN_HEIGHT)
            # Update the position to reflect the average of the wrapped points
            self.position.x = sum([p[0] for p in self.points]) / len(self.points)
            self.position.y = sum([p[1] for p in self.points]) / len(self.points)

        self.position += self.velocity * dt
        self.points = self.polygon()  # Regenerate points based on updated position
        
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
