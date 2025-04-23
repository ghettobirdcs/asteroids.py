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
        self.entered_screen = False

    def draw(self, screen):
        if self.entered_screen:
            for offset in self.get_wrap_offsets():
                pygame.draw.circle(screen, "white", offset, self.radius, 2)

    def update(self, dt):
        if (
            0 + self.radius <= self.position.x <= constants.SCREEN_WIDTH - self.radius and
            0 + self.radius <= self.position.y <= constants.SCREEN_HEIGHT - self.radius
        ):
            self.entered_screen = True

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

    def get_wrap_offsets(self):
        """Returns positions to draw this object for seamless wraparound."""
        positions = []

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                offset = pygame.Vector2(dx * constants.SCREEN_WIDTH, dy * constants.SCREEN_HEIGHT)
                draw_pos = self.position + offset
                if (
                    draw_pos.x + self.radius >= 0 and
                    draw_pos.x - self.radius <= constants.SCREEN_WIDTH and
                    draw_pos.y + self.radius >= 0 and
                    draw_pos.y - self.radius <= constants.SCREEN_HEIGHT
                ):
                    positions.append(draw_pos)

        return positions

    def colliding(self, circle):
        if (self.position.distance_to(circle.position) < self.radius + circle.radius):
            return True
        else:
            return False
