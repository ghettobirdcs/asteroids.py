from circleshape import CircleShape
import constants
import pygame
import random
import math


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.is_visible = False

    def draw(self, screen):
        num_sides = random.randint(5, 7)
        angle_step = 2 * math.pi / num_sides
        points = []

        for i in range(num_sides):
            angle = i * angle_step
            x = self.radius * math.cos(angle)
            y = self.radius * math.sin(angle)
            points.append((x, y))

        pygame.draw.polygon(screen, "white", points, 2)
        # if self.is_visible:
        #     new_points = []
        #     for offset in self.offsets:
        #         for point in points:
        #             new_points.append(point + offset)
        #         pygame.draw.polygon(screen, "white", new_points, 2)

        # WARN: WORKING CODE (CIRCLES):
        # pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        # if self.is_visible:
        #     for offset in self.offsets:
        #         draw_pos = self.position + offset
        #         pygame.draw.circle(screen, "white", draw_pos, self.radius, 2)

    def update(self, dt):
        if (
            self.radius <= self.position.x <= constants.SCREEN_WIDTH - self.radius and
            self.radius <= self.position.y <= constants.SCREEN_HEIGHT - self.radius
        ):
            self.is_visible = True

        if self.is_visible:
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
