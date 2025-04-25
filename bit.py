from shot import Shot
import constants
import random

class Bit(Shot):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.lifetime = 0
        self.radius = 1

    def draw(self, screen):
        super().draw(screen)

    def update(self, dt):
        super().update(dt)
        self.lifetime += 1 * dt
        if self.lifetime > 0.6:
            self.kill()

    def colliding(self, other):
        pass
