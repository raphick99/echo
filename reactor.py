import select
import logging
from exceptions import InvalidReadable


log = logging.getLogger()


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
                    ready_readable.close()
