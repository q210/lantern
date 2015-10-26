# coding: utf-8
import time
from multiprocessing import Process, Queue

from config import HOST, PORT
# from client import TLVClient
from lantern import Lantern
from log import create_logger

logger = create_logger('app', console=True)


def fake_commands(lantern):

    time.sleep(2)
    lantern.power_on()
    time.sleep(2)
    lantern.power_off()
    time.sleep(2)
    lantern.power_on()
    time.sleep(2)
    lantern.set_color('0x00CC00')
    time.sleep(2)
    lantern.power_off()


if __name__ == '__main__':
    logger.debug('starting app')
    console = False

    message_q = Queue()
    message_q.cancel_join_thread()

    if not console:
        # import here to allow app run without any graphic environment at all
        from ui import DCGreenLantern

        lantern_drawing = DCGreenLantern(message_q)
    else:
        lantern_drawing = None

    lantern = Lantern(ui_q=message_q)

    p = Process(target=fake_commands, args=(lantern,))
    p.start()

    lantern_drawing.show()
    p.join()
    logger.debug('Done.')

    # # init TLV client with simple lantern protocol description
    # client = TLVClient(
    #     HOST,
    #     PORT,
    #     protocol={
    #         0x12: lantern.power_on,
    #         0x13: lantern.power_off,
    #         0x20: lantern.set_color,
    #     }
    # )
    #
    # client.listen_commands()
