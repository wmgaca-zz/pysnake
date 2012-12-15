import socket
from lib import config
from lib.types.packages import Package

class SocketHandler(object):

    def __init__(self):
        # Create socket
        print 'Opening socket...'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server
        print 'Trying to connect...'
        self.socket.connect((config.SERVER_HOST, config.SERVER_PORT))
        print 'Connected!'

    def __del__(self):
        self.close()

    def send(self, package):
        assert isinstance(package, Package)

        if self.socket:
            self.socket.sendall(package.serialize())

    def close(self):
        if self.socket:
            self.socket.close()