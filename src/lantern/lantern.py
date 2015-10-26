# coding: utf-8
from log import create_logger

logger = create_logger('lantern', console=True)


class Lantern(object):
    """
    :param ui_q: queue for passing new lantern state to the associated ui
    :param initial: initial state values for this lantern
    """

    _powered = False  # is lantern powered
    _color = '0xFFFFFF'  # lantern color

    def __init__(self, ui_q=None, **initial):
        self.ui_q = ui_q
        self.powered = initial.pop('powered', self._powered)
        self.color = initial.pop('powered', self._color)

    def set_power(self, value):
        """
        Setter for the `powered` attribute. Manages lantern power state.
        True - lantern is On, False - lantern is Off.

        :type value: bool
        :param value: flag should lantern be powered or not
        :rtype: NoneType
        """

        assert isinstance(value, bool), '`powered` value must be a boolean'

        if self.powered != value:
            self._powered = value
            self.send_redraw()

    def set_color(self, rgb_color):
        """
        Setter for the `color` attribute.
        Manages lantern color. Color value must be a bytestring
        representing the RGB colors.

        :type rgb_color: bytestring
        :param rgb_color: hex string of RGB color code
        :rtype: NoneType
        """
        try:
            int(rgb_color, 16)
        except ValueError:
            logger.error('invaid color value:', rgb_color)

        if self.color != rgb_color:
            self._color = rgb_color
            self.send_redraw()

    @property
    def state(self):
        return (self.powered, self.color)

    def send_redraw(self):
        self.ui_q.put(self.state)

    powered = property(lambda self: self._powered, set_power)
    color = property(lambda self: self._color, set_color)

    power_off = lambda self: self.set_power(False)
    power_on = lambda self: self.set_power(True)
