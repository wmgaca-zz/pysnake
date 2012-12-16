import socket
import pickle
import threading
from lib import config
from lib.types.packages import Package

class SocketHandler(object):

    def __init__(self, handler):
        # Create socket
        print 'Opening socket...'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server
        print 'Trying to connect...'
        self.socket.connect((config.SERVER_HOST, config.SERVER_PORT))
        print 'Connected!'

        # Create listening thread
        listening_thread = threading.Thread(target=SocketHandler.listen,
                                            args=(self.socket, handler))
        # Start the thread
        listening_thread.start()

    def __del__(self):
        self.close()

    def send(self, package):
        assert isinstance(package, Package)

        if self.socket:
            self.socket.sendall(package.serialize())

    def close(self):
        if self.socket:
            self.socket.close()

    @staticmethod
    def listen(socket_, handler):
        """Listen on given socket to intercept server's packages.

        Args:
            socket: Socket instance to listen on
            handler: Function called to handle received data
        """

        while True:
            package = pickle.loads(socket_.recv(1024))
            if not package:
                continue
            handler(package)