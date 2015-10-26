# coding: utf-8

from Queue import Empty
from Tkinter import Tk, Canvas, Frame, BOTH

from config import REFRESH_RATE


class DCGreenLanternWidget(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.item = self.canvas.create_rectangle(
            20, 20, 110, 80,
            outline="#fb0", fill="#fb0"
        )
        self.canvas.pack(fill=BOTH, expand=1)

    def set_color(self, color):
        self.canvas.itemconfig(self.item, outline=color, fill=color)


class DCGreenLantern(object):
    dimensions = "140x100"
    title = 'Lantern'

    widget_class = DCGreenLanternWidget

    def __init__(self, message_q):
        self.root = Tk()
        self.widget = self.widget_class(self.root)

        self.root.title(self.title)
        self.root.geometry(self.dimensions)
        self.root.after(REFRESH_RATE, self.check_commands, message_q)

    def check_commands(self, message_q):
        try:
            new_state = message_q.get(0)
            self.redraw(new_state)
        except Empty:
            pass

        finally:
            self.root.after(REFRESH_RATE, self.check_commands, message_q)

    def show(self):
        self.root.mainloop()

    def redraw(self, state):
        self.widget.set_color(state[1].replace('0x', '#'))
