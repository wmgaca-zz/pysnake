import sys
import pygame
from pygame import locals
from lib import config
from lib.net import SocketHandler
from lib.types import packages
from lib.types.packages import UpdateState
from lib.types.snake import Snake, Coords, Direction, Apple

game_objects = []

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

    if isinstance(package, UpdateState):
        global game_objects
        game_objects = package.game_objects

def main():
    surface = init_pygame_env()
    socket_handler = SocketHandler(package_dispatcher)

    # Send handshake
    socket_handler.send(packages.HandShake())

    clock = pygame.time.Clock()

    # Game loop
    while True:
        pygame.draw.rect(surface, pygame.Color('Black'),
                         pygame.Rect(0, 0, config.SCREEN_SIZE[0], config.SCREEN_SIZE[1]),
                         0)

        # Draw game objects
        print 'game objects: %s' % game_objects
        for game_object in game_objects:
            game_object.draw(surface)

        # Refresh the screen
        pygame.display.flip()

        # Get user events
        events = pygame.event.get()

        for event in events:
            if event.type == locals.QUIT:
                socket_handler.send(packages.UserQuit())
                socket_handler.close()
                sys.exit(config.RETURN_OK)

            elif event.type == pygame.KEYDOWN:
                direction = None

                if event.key == locals.K_LEFT:
                    direction = Direction.LEFT
                elif event.key == locals.K_RIGHT:
                    direction = Direction.RIGHT
                elif event.key == locals.K_UP:
                    direction = Direction.UP
                elif event.key == locals.K_DOWN:
                    direction = Direction.DOWN

                # Send snake direction
                if direction:
                    socket_handler.send(packages.UpdateDirection(direction))

        clock.tick(config.FPS)

if __name__ == '__main__':
    main()