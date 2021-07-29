import socket
import logging
import functools
from reactor import Reactor
from exceptions import InvalidReadable
from handlers import handle_server


IP = 'localhost'
PORT = 10000
LISTEN_AMOUNT = 5


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


def create_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    log.info('starting up on {} port {}'.format(IP, PORT))
    server.bind((IP, PORT))

    server.listen(LISTEN_AMOUNT)
    return server


def initialize_echo_server(reactor):
    server = create_server()
    reactor.add_readable(server, functools.partial(handle_server, reactor))


def main():
    reactor = Reactor()
    initialize_echo_server(reactor)
    reactor.run()


if __name__ == '__main__':
    main()
