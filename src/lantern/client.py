# coding: utf-8
import struct
from tornado import tcpclient, ioloop, gen

from log import create_logger

logger = create_logger(__name__)

TLV_SIZES = {
    'tag': 1,
    'length': 2
}


class TLVClient(object):
    stream = None

    def __init__(self, host, port, protocol=None):
        logger.debug('client initialization with host=%s, port=%d', host, port)
        self.host = host
        self.port = port
        self.protocol = protocol or {}

    def _dispatch(self, type_, args):
        """
        dispatch received TLV data to appropriate command based on `self.protocol`
        """
        if type_ not in self.protocol:
            logger.warning('got unknown command in message with type=%s, args=%s', type_, args)
            return

        command = self.protocol[type_]
        if not callable(command):
            logger.error('command %s must be callable', command)
            return

        logger.debug('calling command %s with args %s', command, args)
        try:
            command(*args)
        except Exception:
            logger.exception('error on dispatching command %s with args %s', command, args)

    @gen.coroutine
    def listen_commands(self):
        client = tcpclient.TCPClient()
        stream = yield client.connect(self.host, self.port)

        while not stream.closed():
            res = yield stream.read_bytes(TLV_SIZES['tag'] + TLV_SIZES['length'])
            if not res:
                self.close()
                return

            type_, length = struct.unpack('>BH', res)

            command_args = []
            logger.debug('got message: type=0x%0X, length=%s', type_, length)
            if length != 0:
                raw = yield stream.read_bytes(length)
                if not raw:
                    self.close()
                    raise ValueError('connection was closed before value was sent: type=0x%0X, length=%d', type_, length)

                value = raw
                command_args.append(value)
                logger.debug('got value: %s', repr(value))

            self._dispatch(type_, command_args)

    def start(self):
        self.listen_commands()
        ioloop.IOLoop.instance().start()

    def close(self):
        ioloop.IOLoop.instance().close()

