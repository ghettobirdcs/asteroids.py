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

    def colliding(self, other):
        """Check if this object is colliding with another polygon."""
        # Get the points of both polygons
        poly1 = self.points if hasattr(self, 'points') else [self.position]  # pyright: ignore
        poly2 = other.triangle(pygame.Vector2(0, 0)) if hasattr(other, 'triangle') else [other.points]

        # Get all axes to test (normals of edges from both polygons)
        axes = self.get_axes(poly1) + other.get_axes(poly2)

        # Check for overlap on all axes
        for axis in axes:
            proj1 = self.project_polygon(poly1, axis)
            proj2 = self.project_polygon(poly2, axis)

            if not self.overlap(proj1, proj2):
                # If there's no overlap on any axis, no collision
                return False

        # If there's overlap on all axes, the polygons are colliding
        return True

    def get_axes(self, points):
        """Get the normals of all edges of the polygon."""
        axes = []
        for i in range(len(points)):
            # Get the current and next point
            p1 = pygame.Vector2(points[i])
            p2 = pygame.Vector2(points[(i + 1) % len(points)])

            # Calculate the edge
            edge = p2 - p1

            # Get the normal (perpendicular vector)
            normal = pygame.Vector2(-edge.y, edge.x).normalize()
            axes.append(normal)

        return axes

    def project_polygon(self, points, axis):
        """Project the polygon onto the axis and return the min and max values."""
        min_proj = float('inf')
        max_proj = float('-inf')

        for point in points:
            proj = pygame.Vector2(point).dot(axis)
            min_proj = min(min_proj, proj)
            max_proj = max(max_proj, proj)

        return (min_proj, max_proj)

    def overlap(self, proj1, proj2):
        """Check if two projections overlap."""
        return not (proj1[1] < proj2[0] or proj2[1] < proj1[0])
