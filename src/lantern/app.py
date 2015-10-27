# coding: utf-8
from multiprocessing import Process, Queue

from config import HOST, PORT
from client import TLVClient
from lantern import Lantern
from log import create_logger

logger = create_logger(__name__)


def fake_commands(lantern):

    lantern.power_on()
    lantern.power_off()
    lantern.power_on()
    lantern.set_color('0x00CC00')
    lantern.power_off()


def start_client(lantern):
    # init TLV client with simple lantern protocol description
    client = TLVClient(
        HOST,
        PORT,
        protocol={
            0x12: lantern.power_on,
            0x13: lantern.power_off,
            0x20: lantern.set_color,
        }
    )

    client.listen_commands()
    lantern.terminate()

if __name__ == '__main__':
    logger.debug('starting app')
    console = True

    # message queue for communication between Lantern object and UI
    lantern = Lantern(powered=False, color='0x000000')

    if not console:
        # importing ui here to allow app run without any graphic environment at all
        from ui import DCGreenLantern
        lantern_ui = DCGreenLantern(message_q=lantern.changes_q)
    else:
        from console import ConsoleLantern
        lantern_ui = ConsoleLantern(message_q=lantern.changes_q)

    p = Process(target=fake_commands, args=(lantern,))
    # p = Process(target=start_client, args=(lantern,))

    # start lantern client in forked process
    p.start()

    # draw lantern UI in the main process
    lantern_ui.show()

    # close app when all work is done
    p.join()

    logger.debug('Done.')
