# coding: utf-8

import random
import struct
import time

from tornado import ioloop
from tornado import iostream
from tornado import tcpserver

from lantern.log import create_logger

logger = create_logger(__name__)


class LanternManagementTestServer(tcpserver.TCPServer):
    def handle_stream(self, stream, address):
        logger.info('client %s connected', address)
        for i in range(10):
            msg = random.choice([
                struct.pack('>BH', 0x12, 0),
                struct.pack('>BH', 0x13, 0),
                struct.pack('>BHBBB', 0x20, 3,
                            random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255))
            ])
            try:
                stream.write(msg)
                logger.debug('wrote %s', msg)
            except iostream.StreamClosedError:
                logger.warning('connection with %s was closed unexpectedly', address)
                return

            # not to be too hasty
            time.sleep(1)

        logger.info('closing connection with %s', address)


if __name__ == '__main__':
    server = LanternManagementTestServer()
    server.listen(9999)

    logger.debug('mock server starting on localhost:9999')

    instance = ioloop.IOLoop.instance()
    instance.start()
