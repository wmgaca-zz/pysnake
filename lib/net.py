import socket
import pickle
import threading
import time
from lib import config
from lib.types.packages import Package

class SocketHandler(object):

    _listen = True

    def __init__(self, handler):
        # Create socket
        print 'Opening socket...'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server
        print 'Trying to connect...'
        self.socket.connect((config.SERVER_HOST, config.SERVER_PORT))
        print 'Connected!'

        # Make the socket non-blocking
        self.socket.setblocking(0)

        # Create listening thread
        self.listening_thread = threading.Thread(target=SocketHandler.listen,
                                                 args=(self.socket, handler))
        # Start the thread
        self.listening_thread.start()

    def __del__(self):
        self.close()

    def send(self, package):
        assert isinstance(package, Package)

        if self.socket:
            try:
                self.socket.sendall(package.serialize())
            except socket.error:
                print 'Cannot send package: %s' % package

    def close(self):
        SocketHandler._listen = False
        self.listening_thread.join()

        if self.socket:
            self.socket.close()

    @staticmethod
    def listen(socket_, handler):
        """Listen on given socket to intercept server's packages.

        Args:
            socket: Socket instance to listen on
            handler: Function called to handle received data
        """

        while SocketHandler._listen:
            try:
                data = socket_.recv(100000)
            except socket.error, e:
                time.sleep(0.1)
                continue
            package = pickle.loads(data)
            if not package:
                continue
            handler(package)