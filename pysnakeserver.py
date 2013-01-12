import SocketServer
import pickle
import socket
import threading
import time
import pygame
from lib import config
from lib.types.packages import Package, UserQuit, HandShake, UpdateState, UpdateDirection
from lib.types.snake import Snake, Coords, Apple

class PySnakeHandler(SocketServer.BaseRequestHandler):

    connections = {}
    game_objects = {'apples': []}

    def handle(self):
        print 'Handle new connection.'

        client_id = id(self)

        socket_ = self.request
        socket_.setblocking(0)

        # Add socket to connections list
        PySnakeHandler.connections[client_id] = socket_

        while True:
            try:
                data = socket_.recv(100000)
            except socket.error, e:
                continue

            if not data:
                continue

            package = pickle.loads(data)
            PySnakeHandler.package_dispatcher(package, client_id)

            if isinstance(package, UserQuit):
                return
            if not PySnakeHandler.client_connected(client_id):
                return

    @staticmethod
    def client_connected(client_addr):
        return client_addr in PySnakeHandler.game_objects

    @staticmethod
    def remove_client(client_addr):
        if client_addr in PySnakeHandler.connections:
            del PySnakeHandler.connections[client_addr]
        if client_addr in PySnakeHandler.game_objects:
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
        for client_addr, connection in PySnakeHandler.connections.items():
            try:
                connection.sendall(package.serialize())
            except socket.error:
                print 'Cannot send package %s to %s' % (package, client_addr)
                PySnakeHandler.remove_client(client_addr)


    @staticmethod
    def broadcast_state():
        game_objects = []
        for game_object in PySnakeHandler.game_objects.values():
            if isinstance(game_object, list):
                game_objects.extend(game_object)
            else:
                game_objects.append(game_object)

        PySnakeHandler.__broadcast(UpdateState(game_objects))

def print_user_info():
    while True:
        time.sleep(2)
        print 'Connected users: %s' % len(PySnakeHandler.connections)

def broadcast_state():
    clock = pygame.time.Clock()

    while True:
        if not len(PySnakeHandler.game_objects['apples']):
            PySnakeHandler.game_objects['apples'].append(Apple(Coords.get_random()))

        for game_object in PySnakeHandler.game_objects.values():
            if isinstance(game_object, Snake):
                game_object.move()

        PySnakeHandler.broadcast_state()

        clock.tick(25)

def run_server():
    server = SocketServer.ThreadingTCPServer((config.SERVER_HOST, config.SERVER_PORT),
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