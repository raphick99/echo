import logging
from exceptions import InvalidReadable


log = logging.getLogger()


BLOCK_SIZE = 1024


def handle_server(reactor, server):
    client, addr = server.accept()
    log.info('received new connection from {}, fd is {}'.format(addr, client.fileno()))
    reactor.add_readable(client, handle_client)


def handle_client(client):
    data = client.recv(BLOCK_SIZE)
    if not data:
        raise InvalidReadable()
    log.info('client with fd {} sent: {}. echoing back...'.format(client.fileno(), data))
    client.send(data)
