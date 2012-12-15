import pickle

class Package(object):

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(serialized):
        return pickle.loads(serialized)

class HandShake(Package):
    '''Connect to game.
    '''

    pass

class UpdateDirection(Package):
    '''Send user's direction update.
    '''

    direction = None

    def __init__(self, direction):
        self.direction = direction

    def __str__(self):
        return '<UpdateDirection(direction=%s)>' % self.direction

class UserQuit(Package):
    '''User quits the game.
    '''

    pass

class UserDrop(Package):
    '''Server disconnects the user.
    '''

    pass

class UpdateState(Package):
    '''Game state info.
    '''

    game_objects = None

    def __init__(self, game_objects):
        self.game_objects = game_objects