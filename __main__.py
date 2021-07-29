import socket
import select
import logging


IP = ''
PORT = 10000
LISTEN_AMOUNT = 5


log = logging.basicConfig()


def create_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    log.info('starting up on {} port {}'.format(IP, PORT))
    server.bind((IP, PORT))

    server.listen(LISTEN_AMOUNT)
    return server


def handle_server(server):
    client = server.accpet()
    return client


def main_loop(readables):
    while True:
        ready_fds, _, _ = select.select([i.fileno() for i in readables.keys()], [], [], 0)
        ready_readables = [i for i in readables.keys() if i.fileno() in ready_fds]
        for 




def main():
    main_loop()



if __name__ == '__main__':
    main()
