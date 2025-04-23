import pygame
import constants

# Base class for game objects


class CircleShape(pygame.sprite.Sprite):

    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)  # pyright: ignore
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.is_visible = True
        self.offsets = [
            pygame.Vector2(0, 0),
            pygame.Vector2(constants.SCREEN_WIDTH, 0),
            pygame.Vector2(-constants.SCREEN_WIDTH, 0),
            pygame.Vector2(0, constants.SCREEN_HEIGHT),
            pygame.Vector2(0, -constants.SCREEN_HEIGHT),
            pygame.Vector2(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT),
            pygame.Vector2(-constants.SCREEN_WIDTH, -constants.SCREEN_HEIGHT),
            pygame.Vector2(constants.SCREEN_WIDTH, -constants.SCREEN_HEIGHT),
            pygame.Vector2(-constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        ]

    def draw(self, screen):
        pass

    def update(self, dt):
        # Wrap around horizontally
        if self.position.x - self.radius < 0:
            self.position.x += constants.SCREEN_WIDTH
        elif self.position.x + self.radius > constants.SCREEN_WIDTH:
            self.position.x -= constants.SCREEN_WIDTH

        # Wrap around vertically
        if self.position.y - self.radius < 0:
            self.position.y += constants.SCREEN_HEIGHT
        elif self.position.y + self.radius > constants.SCREEN_HEIGHT:
            self.position.y -= constants.SCREEN_HEIGHT

    def colliding(self, circle):
        if (self.position.distance_to(circle.position) < self.radius + circle.radius):
            return True
        else:
            return False
