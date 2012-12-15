
class Sprite(object):

    coords = None
    updated = True
    surface = None

    def __init__(self, coords, surface):
        self.coords = coords
        self.updated = True
        self.surface = surface

    def _draw(self):
        raise NotImplementedError

    def draw(self):
        self._draw()
        self.updated = False