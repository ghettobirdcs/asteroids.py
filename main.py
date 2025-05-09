# import sys
import pygame
import constants
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

# TODO: Add comments
def draw_lives(screen, player, lives):
    radius = player.radius // 2
    for i in range(lives):
        offset_x = 32 + i * (radius * 2 + 10)
        offset_y = constants.SCREEN_HEIGHT - 40

        forward = pygame.Vector2(0, -1)
        right = pygame.Vector2(1, 0) * radius / 1.5

        a = pygame.Vector2(offset_x, offset_y) + forward * radius
        b = pygame.Vector2(offset_x, offset_y) - forward * radius - right
        c = pygame.Vector2(offset_x, offset_y) - forward * radius + right

        pygame.draw.polygon(screen, "green", [a, b, c])

def draw_replay_screen(screen, score):
    font = pygame.font.Font(None, 48)

    """Draw the replay screen with game over text and score."""
    screen.fill("black")  # Clear the screen once

    # Draw "Game Over" text
    text = font.render("Game Over! Press R to Replay", True, "white")
    screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2,
                       constants.SCREEN_HEIGHT // 2 - text.get_height() // 2))

    # Draw score text
    text_2 = font.render(f"SCORE: {score}", True, (255, 255, 255))
    screen.blit(text_2, (constants.SCREEN_WIDTH // 2 - text_2.get_width() // 2,
                         constants.SCREEN_HEIGHT // 2 - text_2.get_height() // 2 - 40))

    pygame.display.flip()  # Update the display after drawing everything

def reset_game(updateable, drawable, asteroids, shots):
    """Reset the game state for replay."""
    updateable.empty()
    drawable.empty()
    asteroids.empty()
    shots.empty()

    # Reinitialize player and asteroid field
    player = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    return player, asteroid_field

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {constants.SCREEN_WIDTH}")
    print(f"Screen height: {constants.SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (drawable, updateable)  # pyright: ignore
    Asteroid.containers = (asteroids, updateable, drawable)  # pyright: ignore
    AsteroidField.containers = (updateable)  # pyright: ignore
    Shot.containers = (shots, drawable, updateable)  # pyright: ignore

    player, asteroid_field = reset_game(updateable, drawable, asteroids, shots)

    # Amount of extra lives to grant the player
    extra_lives = constants.PLAYER_EXTRA_LIVES

    # Setup variables for displaying score and extra lives
    pygame.font.init()
    font = pygame.font.Font(None, 32)
    score = 0
    score_x = 32
    score_y = 32
    dead = False
    game_over = False
    current_threshold = 0
    score_rate = constants.SCORE_RATE  # Score increase per second

    while (True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if game_over:
            player.kill()
            draw_replay_screen(screen, score)

            # Wait for player to press "R" to replay
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Reset game state
                player, asteroid_field = reset_game(updateable, drawable, asteroids, shots)
                score = 0
                extra_lives = constants.PLAYER_EXTRA_LIVES
                game_over = False
            continue

        if dead:
            player.kill()

            # Respawn the player
            player = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
            player.invulnerability_timer = 2.5  # pyright: ignore
            dead = False

            continue

        screen.fill("black")

        score_text = font.render(f"SCORE: {score}", True, "white")
        screen.blit(score_text, (score_x, score_y))
        # Score increases for staying alive
        score += int(score_rate * dt)

        draw_lives(screen, player, extra_lives)

        updateable.update(dt)

        for asteroid in asteroids:
            if asteroid.colliding(player) and player.invulnerability_timer <= 0:
                if extra_lives > 0:
                    extra_lives -= 1
                    dead = True
                    score -= 15000
                else:
                    game_over = True

        for asteroid in asteroids:
            for bullet in shots:
                if bullet.colliding(asteroid):
                    asteroid.split()
                    bullet.kill()
                    score += 750

        # Player gains extra lives for gaining score
        new_threshold = score // constants.SCORE_THRESHOLD
        if new_threshold > current_threshold:
            extra_lives += 1
            current_threshold = new_threshold

        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()
        dt = clock.tick(constants.FPS) / 1000


if __name__ == "__main__":
    main()
