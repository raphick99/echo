import socket
import select
import logging
import functools


IP = 'localhost'
PORT = 10000
LISTEN_AMOUNT = 5
BLOCK_SIZE = 1024


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


class InvalidReadable(Exception):
    pass


def create_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    log.info('starting up on {} port {}'.format(IP, PORT))
    server.bind((IP, PORT))

    server.listen(LISTEN_AMOUNT)
    return server


def handle_server(reactor, server):
    client, addr = server.accept()
    log.info('received new connection from {}'.format(addr))
    reactor.add_readable(client, handle_client)


def handle_client(client):
    data = client.recv(BLOCK_SIZE)
    if not data:
        raise InvalidReadable()
    log.info('client with fd {} sent: {}. echoing back...'.format(client.fileno(), data))
    client.send(data)


class Reactor(object):
    def __init__(self):
        self.readables = {}

    def remove_readable(self, readable_to_remove):
        self.readables.pop(readable_to_remove)

    def add_readable(self, readable_to_add, handler):
        self.readables[readable_to_add] = handler

    def run(self):
        while True:
            ready_fds, _, _ = select.select([i.fileno() for i in self.readables.keys()], [], [])
            ready_readables = [i for i in self.readables.keys() if i.fileno() in ready_fds]
            for ready_readable in ready_readables:
                try:
                    self.readables[ready_readable](ready_readable)
                except InvalidReadable:
                    log.info('client with fd {} closed connection'.format(ready_readable.fileno()))
                    self.readables.pop(ready_readable)


def initialize_echo_server(reactor):
    server = create_server()
    reactor.add_readable(server, functools.partial(handle_server, reactor))


def main():
    reactor = Reactor()
    initialize_echo_server(reactor)
    reactor.run()


if __name__ == '__main__':
    main()
