# coding: utf-8
import struct
from tornado import tcpclient, ioloop, gen
from tornado.gen import Return
from tornado.iostream import StreamClosedError

from log import create_logger

logger = create_logger(__name__)

# our TLV specs
TLV_SIZES = {
    'tag': 1,
    'length': 2
}


class TLVClient(object):
    """
    TCP client that will receive TLV data, unpack them and call commands based on `protocol`.

    :type host: basestring
    :param host: hostname to connect
    :type port: int
    :param port: port to connect

    :type protocol: dict{int: callable}
    :param protocol: protocol which will be mathed to the received TLV data.
    """
    stream = None

    def __init__(self, host, port, protocol=None):
        logger.debug('client initialization with host=%s, port=%d', host, port)
        self.host = host
        self.port = port
        self.protocol = protocol or {}

    def _dispatch(self, type_, args):
        """
        Dispatch received TLV data to appropriate command based on `self.protocol`
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
        except (TypeError, ValueError) as exc:
            logger.error('error in protocol implementation for command %s with args %s: %s', command, args, repr(exc))
        except Exception as exc:
            logger.exception('error on dispatching command %s with args %s', command, args)

    @gen.coroutine
    def connect(self):
        """
        Connect to specified host:port
        """
        client = tcpclient.TCPClient()
        try:
            stream = yield client.connect(self.host, self.port)
        except IOError as exc:
            logger.error("failed to connect: %s", repr(exc))
            self.stop()
        else:
            raise Return((stream))

    @gen.coroutine
    def receive_commands(self, stream):
        """
        Read commands in TLV

        :return: command and command arguments as a tuple
        """
        try:
            # read command type
            type_data = yield stream.read_bytes(TLV_SIZES['tag'] + TLV_SIZES['length'])

            type_, length = struct.unpack('>BH', type_data)

            # read command arguments, if any
            command_args = []
            logger.debug('got message: type=0x%0X, length=%s', type_, length)
            if length != 0:
                value = yield stream.read_bytes(length)
                if not value:
                    logger.error('connection was closed before value was sent: type=0x%0X, length=%d', type_, length)

                command_args.append(value)
                logger.debug('got value: %s', repr(value))

        except StreamClosedError as exc:
            logger.debug('stream was closed')
            self.stop()

        except Exception as exc:
            logger.exception('unhandled exception: %s', repr(exc))
            self.stop()

        else:
            raise Return((type_, command_args))

    @gen.coroutine
    def add_commands_handler(self):
        stream = yield self.connect()
        while not stream.closed():
            type_, command_args = yield self.receive_commands(stream)

            # call received command
            self._dispatch(type_, command_args)

    def start(self):
        logger.debug('IOloop starting')

        self.add_commands_handler()
        ioloop.IOLoop.instance().start()

    def stop(self):
        ioloop.IOLoop.instance().stop()
        logger.debug('IOloop stopped')

