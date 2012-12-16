
class Sprite(object):

    coords = None
    updated = True

    def __init__(self, coords):
        self.coords = coords
        self.updated = True

    def _draw(self, surface):
        raise NotImplementedError

    def draw(self, surface):
        self._draw(surface)
        self.updated = False