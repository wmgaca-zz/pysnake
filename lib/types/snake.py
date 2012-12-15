import random
import pygame
from lib import config
from lib.types import sprite

class Coords(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '<Coords(%s, %s)>' % (self.x, self.y)

    def __repr__(self):
        return str(self)

    def moved(self, direction, distance=1):
        """Create new Coords object with coordinates moved to a given direction.
        """
        
        coords = Coords(self.x, self.y)
        coords.move(direction, distance)
        return coords

    def move(self, direction, distance=1):
        """Move coords to the given direction.
        """

        if direction == Direction.UP:
            self.y -= distance
        elif direction == Direction.DOWN:
            self.y += distance
        elif direction == Direction.LEFT:
            self.x -= distance
        elif direction == Direction.RIGHT:
            self.x += distance

        self.x %= config.SCREEN_SIZE[0] / config.TILE_SIZE[0]
        self.y %= config.SCREEN_SIZE[1] / config.TILE_SIZE[1]
        
class Direction(object):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    @classmethod
    def are_opposite(cls, a, b):
        if a == b:
            return False
        if a == cls.UP and b == cls.DOWN:
            return True
        if b == cls.UP and a == cls.DOWN:
            return True
        if a == cls.LEFT and b == cls.RIGHT:
            return True
        if b == cls.LEFT and a == cls.RIGHT:
            return True
        return False

def draw_tile(coords, color, surface):
   
    rect = pygame.Rect(coords.x * config.TILE_SIZE[0], 
                       coords.y * config.TILE_SIZE[1], 
                       config.TILE_SIZE[0], 
                       config.TILE_SIZE[1])

    pygame.draw.rect(surface, color, rect)

class Snake(sprite.Sprite):

    _direction = Direction.RIGHT
    position = []
    
    def __init__(self, coords, surface):
        super(Snake, self).__init__(coords, surface)

        self.position = [coords, coords.moved(Direction.LEFT)]

        print self.position

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_direction):
        if not new_direction:
            return
        if Direction.are_opposite(self._direction, new_direction):
            return
        self._direction = new_direction

    def _draw(self):
        for position in self.position:
            draw_tile(coords=position, 
                      color=pygame.Color('Red'), 
                      surface=self.surface)

    def move(self):
        # Get rid of the last element
        self.position.pop(-1)

        # Add new element to the head
        self.position.insert(0, self.position[0].moved(self.direction))

        # Updated, should be drawn
        self.updated = True

class Apple(sprite.Sprite):

    def __init__(self, coords, surface):
        super(Apple, self).__init__(coords, surface)

    def _draw(self):
        draw_tile(coords=self.coords,
                  color=pygame.Color('Green'),
                  surface=self.surface)

    @staticmethod
    def get_random(surface):
        coords = Coords(random.randint(0, config.SCREEN_SIZE[0] // config.TILE_SIZE[0]),
                        random.randint(0, config.SCREEN_SIZE[1] // config.TILE_SIZE[1]))
        return Apple(coords, surface)