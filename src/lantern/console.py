# coding: utf-8
from Queue import Empty

from config import DEFAULT_POWERED, DEFAULT_COLOR, REFRESH_RATE
from log import create_logger

logger = create_logger(__name__)


class ConsoleLantern(object):
    """
    Simple lantern state change representation in console
    """
    initial_msg = 'Lantern initialized. Default state: %s, color %s'
    state_chane_msg = 'New state: %s, color: %s'

    def __init__(self, message_q):
        self.message_q = message_q

    def show(self):
        print self.initial_msg % ('ON' if DEFAULT_POWERED else 'OFF', DEFAULT_COLOR)

        while True:
            try:
                new_state = self.message_q.get(block=True, timeout=REFRESH_RATE / 1000.0)  # timeout value in seconds
                if new_state is None:
                    logger.debug('termination signal received')
                    break
                print self.state_chane_msg % ('ON' if new_state[0] else 'OFF', new_state[1])

            except Empty:
                pass
            except KeyboardInterrupt:
                logger.debug('interrupted from keyboard')
                break
