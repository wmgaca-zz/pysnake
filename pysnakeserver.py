import SocketServer
from lib import config
import pickle

class PySnakeHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # Read data from request
        while True:

            self.data = pickle.loads(self.request.recv(1024))

            if not self.data:
                continue

            # Print the data
            print "[%s] %s: data: %s" % (id(self), self.client_address[0], self.data)

            # Resend data
            #self.request.sendall(self.data)

def run_server():
    server = SocketServer.TCPServer((config.SERVER_HOST, config.SERVER_PORT),
                                    PySnakeHandler)
    print 'Running server on %s:%s' % (config.SERVER_HOST, config.SERVER_PORT)
    server.serve_forever()

if __name__ == '__main__':
    run_server()