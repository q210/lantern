# coding: utf-8

from Queue import Empty
from Tkinter import Tk, Canvas, Frame, BOTH

from config import REFRESH_RATE, DIMENSIONS, BACKGROUND_COLOR
from log import create_logger

logger = create_logger(__name__)

SCALE = 0.8  # ui scalling coefficient


class DCGreenLanternWidget(Frame):
    """
    Green Lantern logo from DC comics
    (yeah yeah, i'm shitty artist, i know)
    """
    green = "#07A007"
    outline = "#FFFFFF"
    unpowered = '#C0C0C0'

    def __init__(self, parent, initial_state):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self, cnf={'background': BACKGROUND_COLOR})

        # outer circle
        kw = {'outline': self.outline, 'fill': self.green}
        base = 30 * SCALE
        d = 190 * SCALE
        s = 10 * SCALE
        outer_circle = (
            (base, base, base + d - s, base + d),
            (base + s, base + s, base + d - s - s, base + d - s)
        )
        self.canvas.create_oval(*outer_circle[0], **kw)

        kw['fill'] = BACKGROUND_COLOR
        self.canvas.create_oval(*outer_circle[1], **kw)

        # inner circle
        kw = {'outline': self.outline, 'fill': self.green}
        base = 70 * SCALE
        d = 100 * SCALE
        s = 14 * SCALE
        outer_circle = (
            (base, base + s, base + d, base + d),
            (base + s, base + s + s, base + d - s, base + d - s)
        )
        self.canvas.create_oval(*outer_circle[0], **kw)

        kw['fill'] = initial_state[1] if initial_state[0] else self.unpowered
        self.item = self.canvas.create_oval(*outer_circle[1], **kw)

        # top bar
        self.canvas.create_rectangle(
            base, base, base + d, base + s,
            outline=self.green, fill=self.green
        )

        # bottom bar
        self.canvas.create_rectangle(
            base, base + d, base + d, base + d + s,
            outline=self.green, fill=self.green
        )
        self.canvas.pack(fill=BOTH, expand=1)

    def change_color(self, color):
        self.canvas.itemconfig(self.item, outline=color, fill=color)


class DCGreenLantern(object):
    """
    This class is responsible for redrawing UI widget
    """
    dimensions = DIMENSIONS
    title = 'Green Lantern'

    widget_class = DCGreenLanternWidget

    def __init__(self, message_q, initial_state):
        self.root = Tk()
        self.widget = self.widget_class(self.root, initial_state)

        self.root.title(self.title)
        self.root.geometry(self.dimensions)
        self.root.after(REFRESH_RATE, self.check_commands, message_q)

    def check_commands(self, message_q):
        """
        Check queue for messages with new lantern state and redraw UI.
        Close UI if there is None value in the queue.

        :type message_q: multiprocessing.Queue
        """
        try:
            new_state = message_q.get(block=True, timeout=REFRESH_RATE / 1000.0)  # timeout value in seconds
            if new_state is None:
                logger.debug('termination signal received')
                self.root.quit()
                return

            self.redraw(new_state)
        except Empty:
            pass

        self.root.after(REFRESH_RATE, self.check_commands, message_q)

    def show(self):
        self.root.mainloop()

    def redraw(self, state):
        assert isinstance(state[1], basestring), 'color must be a string'
        self.widget.change_color(state[1])
