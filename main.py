import sys
import pygame
import constants
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

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

    player = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # Setup font to be used for displaying the score
    pygame.font.init()
    font = pygame.font.Font(None, 32)
    score_x = 32
    score_y = 32

    score = 0
    game_over = False

    while (True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if game_over:
            screen.fill("black")
            font = pygame.font.Font(None, 48)
            replay_text = font.render("Game Over! Press R to Replay", True, (255, 255, 255))
            replay_text_2 = font.render(f"SCORE: {score}", True, (255, 255, 255))
            screen.blit(replay_text, (constants.SCREEN_WIDTH / 2 - replay_text.get_width() / 2,
                                      constants.SCREEN_HEIGHT / 2 - replay_text.get_height() / 2))
            screen.blit(replay_text_2, (constants.SCREEN_WIDTH / 2 - replay_text_2.get_width() / 2,
                                      constants.SCREEN_HEIGHT / 2 - replay_text_2.get_height() - 25))
            pygame.display.flip()

            # Wait for player to press "R" to replay
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Reset game state
                player, asteroid_field = reset_game(updateable, drawable, asteroids, shots)
                score = 0
                game_over = False
            continue

        screen.fill("black")

        score_text = font.render(f"SCORE: {score}", True, "white")
        screen.blit(score_text, (score_x, score_y))
        # Score increases for staying alive
        score += 1

        updateable.update(dt)

        for asteroid in asteroids:
            if asteroid.colliding(player):
                # TODO: Add a way to replay, extra lives, score
                print(f"Game Over!\nSCORE: {score}")
                game_over = True

        for asteroid in asteroids:
            for bullet in shots:
                if bullet.colliding(asteroid):
                    asteroid.split()
                    bullet.kill()
                    score += 1000

        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
