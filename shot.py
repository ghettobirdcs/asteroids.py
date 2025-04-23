import pygame
import constants
from circleshape import CircleShape


class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, constants.SHOT_RADIUS)

    def draw(self, screen):
        for offset in self.offsets:
            draw_pos = self.position + offset
            pygame.draw.circle(screen, "white", draw_pos, self.radius, 2)

    def update(self, dt):
        super().update(dt)
        self.position += self.velocity * dt
