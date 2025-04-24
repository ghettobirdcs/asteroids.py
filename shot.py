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

    def colliding(self, other):
        """Check if this shot is colliding with another object (circle or polygon)."""
        # If the other object has a points attribute, use it
        if hasattr(other, 'points'):
            points = other.points
        # Otherwise, assume the other object is a circle and check circular collision
        else:
            return self.position.distance_to(other.position) <= self.radius + other.radius  # pyright: ignore
    
        # Check collision with the edges of the polygon
        for i in range(len(points)):
            # Get the current and next vertex to form an edge
            p1 = pygame.Vector2(points[i])
            p2 = pygame.Vector2(points[(i + 1) % len(points)])  # Wrap around to the first point
    
            # Check if the circle intersects this edge
            if self.circle_intersects_edge(p1, p2):
                return True
    
        return False
    
    def circle_intersects_edge(self, p1, p2):
        """Check if the circle intersects a line segment (edge) defined by p1 and p2."""
        # Vector from p1 to p2
        edge = p2 - p1
        edge_length_squared = edge.length_squared()
    
        # Vector from p1 to the circle center
        circle_vec = self.position - p1
    
        # Project the circle's center onto the edge (clamping t between 0 and 1)
        t = max(0, min(1, circle_vec.dot(edge) / edge_length_squared))
    
        # Find the closest point on the edge to the circle's center
        closest_point = p1 + t * edge
    
        # Check if the closest point is within the circle's radius
        return self.position.distance_to(closest_point) <= self.radius  # pyright: ignore
