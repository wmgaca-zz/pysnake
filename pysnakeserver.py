import SocketServer
import pickle
import socket
import threading
import time
from lib import config
from lib.types.packages import Package, UserQuit, HandShake, UpdateState, UpdateDirection
from lib.types.snake import Snake, Coords

class PySnakeHandler(SocketServer.BaseRequestHandler):

    connections = {}
    game_objects = {}

    def handle(self):
        socket_ = self.request
        socket_.setblocking(0)

        # Add socket to connections list
        PySnakeHandler.connections[self.client_address[0]] = socket_

        while True:
            try:
                data = socket_.recv(100000)
            except socket.error, e:
                continue

            if not PySnakeHandler.client_connected(self.client_address[0]):
                return

            if not data:
                continue

            package = pickle.loads(data)

            PySnakeHandler.package_dispatcher(package,
                                              self.client_address[0])

            if isinstance(package, UserQuit):
                return

    @staticmethod
    def client_connected(client_addr):
        return client_addr in PySnakeHandler.game_objects

    @staticmethod
    def remove_client(client_addr):
        del PySnakeHandler.connections[client_addr]
        del PySnakeHandler.game_objects[client_addr]

    @staticmethod
    def package_dispatcher(package, client_addr):
        assert isinstance(package, Package)

        if isinstance(package, UserQuit):
            PySnakeHandler.remove_client(client_addr)
        elif isinstance(package, HandShake):
            PySnakeHandler.game_objects[client_addr] = Snake(Coords.get_random())
        elif isinstance(package, UpdateDirection):
            if client_addr in PySnakeHandler.game_objects:
                PySnakeHandler.game_objects[client_addr].direction = package.direction

    @staticmethod
    def __broadcast(package):
        for client_addr, connection in PySnakeHandler.connections:
            try:
                connection.sendall(package.serialize())
            except socket.error:
                print 'Cannot send package %s to %s' % (package, client_addr)
                PySnakeHandler.remove_client(client_addr)


    @staticmethod
    def broadcast_state():
        PySnakeHandler.__broadcast(UpdateState(PySnakeHandler.game_objects.values()))

def print_user_info():
    while True:
        time.sleep(1)
        print 'Connected users: %s' % len(PySnakeHandler.connections)

def broadcast_state():
    while True:
        time.sleep(0.05)
        for game_object in PySnakeHandler.game_objects.values():
            if isinstance(game_object, Snake):
                game_object.move()
        PySnakeHandler.broadcast_state()

def run_server():
    server = SocketServer.TCPServer((config.SERVER_HOST, config.SERVER_PORT),
                                    PySnakeHandler)

    user_info_thread = threading.Thread(target=print_user_info)
    user_info_thread.start()

    broadcast_state_thread = threading.Thread(target=broadcast_state)
    broadcast_state_thread.start()

    print 'Running server on %s:%s' % (config.SERVER_HOST, config.SERVER_PORT)
    server.serve_forever()

    user_info_thread.join()

if __name__ == '__main__':
    run_server()