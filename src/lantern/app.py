# coding: utf-8
import struct
import optparse
from multiprocessing import Process

from config import HOST, PORT, DEFAULT_POWERED, DEFAULT_COLOR
from client import TLVClient
from lantern import Lantern
from log import create_logger

logger = create_logger(__name__)


parser = optparse.OptionParser()
parser.add_option("-c", "--color", type="string",
                  default=DEFAULT_COLOR,
                  help="initial lantern color")
parser.add_option("-p", "--powered",
                  action="store_true", default=DEFAULT_POWERED,
                  help="initial lantern power state")
parser.add_option("--console",
                  action="store_true", default=False,
                  help="use console lantern")


def start_client(lantern):
    """
    Starting TLV client with simple lantern protocol implementation

    :type lantern: Lantern
    """

    def _set_color_from_bytes(bytestruct):
        """
        To keep protocol easy to read, converting bytes to RGB color string
        right here using clojure
        """
        rgb_color = '#%0X%0X%0X' % struct.unpack('>BBB', bytestruct)
        lantern.set_color(rgb_color)

    client = TLVClient(
        HOST,
        PORT,
        protocol={
            0x12: lantern.power_on,
            0x13: lantern.power_off,
            0x20: _set_color_from_bytes,
        }
    )

    try:
        client.start()
    except KeyboardInterrupt:
        logger.info('client was interrupted from keyboard')


if __name__ == '__main__':
    logger.debug('starting app')
    (options, args) = parser.parse_args()

    # Lantern object with message queue for communication with UI
    lantern = Lantern(powered=options.powered, color=options.color)

    if not options.console:
        # importing ui here to allow app run without any graphic environment at all
        from ui import DCGreenLantern
        lantern_ui = DCGreenLantern(message_q=lantern.changes_q)
    else:
        from console import ConsoleLantern
        lantern_ui = ConsoleLantern(message_q=lantern.changes_q)

    p = Process(target=start_client, args=(lantern,))

    # start lantern client in forked process
    p.start()

    # draw lantern UI in the main process
    lantern_ui.show()

    # close app when all work is done
    p.join()

    logger.debug('Done.')
