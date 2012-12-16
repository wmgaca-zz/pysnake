import SocketServer
import pickle
import socket
from lib import config
from lib.types.packages import Package

class PySnakeHandler(SocketServer.BaseRequestHandler):

    connections = {}

    def handle(self):
        socket_ = self.request
        socket_.setblocking(0)

        # Add socket to connections list
        PySnakeHandler.connections[self.client_address[0]] = socket_

        while True:
            try:
                data = socket_.recv(1024)
            except socket.error, e:
                continue

            if not data:
                continue

            package = pickle.loads(data)

            # Print the data
            print "[%s] %s: data: %s" % (id(self), self.client_address[0], package)

            PySnakeHandler.package_dispatcher(package,
                                              self.client_address[0])

    @classmethod
    def package_dispatcher(cls, package, client_addr):
        assert isinstance(package, Package)


def run_server():
    server = SocketServer.TCPServer((config.SERVER_HOST, config.SERVER_PORT),
                                    PySnakeHandler)
    print 'Running server on %s:%s' % (config.SERVER_HOST, config.SERVER_PORT)
    server.serve_forever()

if __name__ == '__main__':
    run_server()