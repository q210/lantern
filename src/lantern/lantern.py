# coding: utf-8
from functools import wraps
from multiprocessing import Queue

from log import create_logger
from config import DEFAULT_POWERED, DEFAULT_COLOR

logger = create_logger(__name__)


def redraw_on_change(meth):
    """
    Decorator.
    Sends redraw message if lantern state changes.
    :param meth: lantern method
    """
    @wraps(meth)
    def _inner(obj, *args, **kwargs):
        old_state = obj.state

        meth(obj, *args, **kwargs)

        if old_state != obj.state:
            obj._send_redraw()

    return _inner


class Lantern(object):
    # variables to hold lantern state
    _powered = DEFAULT_POWERED
    _color = DEFAULT_COLOR

    def __init__(self, powered=DEFAULT_POWERED, color=DEFAULT_COLOR):
        # queue for lantern state changes
        # will be used for communication between Lantern object and UI
        self.changes_q = Queue()
        self.changes_q.cancel_join_thread()

        # set initial state
        self.powered = powered
        self.color = color

    @property
    def state(self):
        """
        Return lantern state as a tuple
        """
        return (self.powered, self.color)

    @redraw_on_change
    def set_power(self, value):
        """
        Setter for the `powered` attribute. Manages lantern power state.
        True - lantern is On, False - lantern is Off.

        :type value: bool
        :param value: flag should lantern be powered or not
        :rtype: NoneType
        """
        if not isinstance(value, bool):
            raise ValueError('`powered` value must be a boolean')

        else:
            self._powered = value

    @redraw_on_change
    def set_color(self, rgb_color):
        """
        Setter for the `color` attribute.
        Manages lantern color. Color value must be a string in format '#FFFFFF'
        representing the RGB colors.

        :type rgb_color: string
        :param rgb_color: hex string of RGB color code
        :rtype: NoneType
        """
        try:
            val = int(rgb_color.lstrip('#'), 16)
            if val < 0x000000 or val > 0xFFFFFF:
                raise ValueError('invaid color value:', rgb_color)
        except ValueError:
            logger.error('invaid color value: %s', rgb_color)

        else:
            self._color = rgb_color

    def _send_redraw(self):
        """
        Send lantern current state to the message queue to cause UI redraw
        """
        self.changes_q.put(self.state)

    powered = property(lambda self: self._powered, set_power)
    color = property(lambda self: self._color, set_color)

    power_off = lambda self: self.set_power(False)
    power_on = lambda self: self.set_power(True)
