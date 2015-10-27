# coding: utf-8
import sys
import random
import struct
import time

from tornado import ioloop, iostream, tcpserver

from lantern.config import PORT
from lantern.log import create_logger

logger = create_logger(__name__)


class LanternManagementTestServer(tcpserver.TCPServer):
    prepared_commands = None

    def handle_stream(self, stream, address):
        logger.info('client %s connected', address)
        for command in self.prepared_commands:
            if command is None:
                sys.exit(1)

            try:
                stream.write(command)
                logger.debug('wrote %s', command)
            except iostream.StreamClosedError:
                logger.warning('connection with %s was closed unexpectedly', address)
                return

            # not to be too hasty
            time.sleep(.5)

        logger.info('closing connection with %s', address)


if __name__ == '__main__':
    server = LanternManagementTestServer()

    logger.debug('mock server starting on localhost:%d' % PORT)

    commands = []
    for i in range(10):
        commands.append(
            random.choice([
                struct.pack('>BH', 0x12, 0),
                struct.pack('>BH', 0x13, 0),
                struct.pack('>BHBBB', 0x20, 3,
                            random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255))
            ])
        )

    server.prepared_commands = commands
    server.listen(PORT)
    instance = ioloop.IOLoop.instance()
    instance.start()
