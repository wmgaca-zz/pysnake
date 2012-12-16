import sys
import pygame
from pygame import locals
from lib import config
from lib.net import SocketHandler
from lib.types import packages
from lib.types.snake import Snake, Coords, Direction, Apple

def init_pygame_env():
    """Initialize pygame environment.
    """

    pygame.init()
    window = pygame.display.set_mode(config.SCREEN_SIZE)
    pygame.display.set_caption(config.CAPTION)
    surface = pygame.display.get_surface()

    return surface

def package_dispatcher(package):
    """Dispatch package received from the server.
    """

    print 'Dispatching: %s' % package

def main():
    surface = init_pygame_env()
    snake = Snake(Coords(2, 2), surface=surface)
    game_objects = [snake, Apple.get_random(surface)]
    socket_handler = SocketHandler()

    # Send handshake
    socket_handler.send(packages.HandShake())

    clock = pygame.time.Clock()

    # Game loop
    while True:
        pygame.draw.rect(surface, pygame.Color('Black'),
                         pygame.Rect(0, 0, config.SCREEN_SIZE[0], config.SCREEN_SIZE[1]),
                         0)

        # Draw game objects
        for game_object in game_objects:
            game_object.draw()

        # Draw something
        pygame.draw.line(surface, pygame.Color('White'), (10, 10,), (100, 100,), 5)

        # Refresh the screen
        pygame.display.flip()

        # Get user events
        events = pygame.event.get()

        for event in events:
            if event.type == locals.QUIT:
                socket_handler.send(packages.UserQuit())
                sys.exit(config.RETURN_OK)

            elif event.type == pygame.KEYDOWN:
                if event.key == locals.K_LEFT:
                    snake.direction = Direction.LEFT
                elif event.key == locals.K_RIGHT:
                    snake.direction = Direction.RIGHT
                elif event.key == locals.K_UP:
                    snake.direction = Direction.UP
                elif event.key == locals.K_DOWN:
                    snake.direction = Direction.DOWN
                    print "DOWN!!"

        # Send snake direction
        socket_handler.send(packages.UpdateDirection(snake.direction))

        snake.move()

        clock.tick(config.FPS)

if __name__ == '__main__':
    main()