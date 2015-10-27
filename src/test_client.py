# coding: utf-8

import struct
from Queue import Empty
from functools import partial
from contextlib import contextmanager
from multiprocessing import Process
from tornado import ioloop

from lantern.app import start_client
from lantern.config import PORT
from lantern.lantern import Lantern
from mock_server import LanternManagementTestServer

LANTERN_ON = struct.pack('>BH', 0x12, 0)
LANTERN_OFF = struct.pack('>BH', 0x13, 0)
CHANGE_BYTES = partial(struct.pack, '>BHBBB', 0x20, 3)
CHANGE_COLOR = lambda col: CHANGE_BYTES(*
    map(lambda *num: int(''.join(num), 16), *(iter(col.lstrip('#')),) * 2)
)


@contextmanager
def mock_serve(commands, port=PORT):
    def _serve(commands_list):
        server = LanternManagementTestServer()
        server.listen(port)
        server.prepared_commands = commands_list
        instance = ioloop.IOLoop.instance()
        instance.start()

    lantern = Lantern()
    server_process = Process(target=_serve, args=(commands,))
    lantern_process = Process(target=start_client, args=(lantern,))

    server_process.start()
    lantern_process.start()

    yield lantern

    lantern_process.join()
    server_process.terminate()


def _collect_states(lantern):
    states = []
    while True:
        try:
            new_state = lantern.changes_q.get(block=False)
            if new_state is None:
                break

            states.append(new_state)

        except Empty:
            pass

    return states


def test_normal_flow():
    commands = [
        LANTERN_ON,
        CHANGE_COLOR('#A0A0A0'),
        LANTERN_OFF
    ]
    with mock_serve(commands) as lantern:
        states = _collect_states(lantern)

    assert states == [(True, '#000000'), (True, '#A0A0A0'), (False, '#A0A0A0')]


def test_cant_connect():
    with mock_serve([], port=5555) as lantern:
        states = _collect_states(lantern)

    assert states == []


def test_sudden_disconnect():
    # disconnect between commands
    with mock_serve([LANTERN_ON, None, LANTERN_OFF]) as lantern:
        states = _collect_states(lantern)

    assert states == [(True, '#000000')]

    # disconnect when reading command
    with mock_serve([CHANGE_COLOR('#ABCAFF'), struct.pack('>BHB', 0x20, 3, 12), None, LANTERN_OFF]) as lantern:
        states = _collect_states(lantern)

    assert states == [(False, '#ABCAFF')]


def test_unknown_command():
    with mock_serve([LANTERN_ON, struct.pack('>BHB', 0x21, 1, 1)]) as lantern:
        states = _collect_states(lantern)

    assert states == [(True, '#000000')]


def test_wrong_format():
    with mock_serve([LANTERN_ON, struct.pack('>BHB', 0x13, 1, 1)]) as lantern:
        states = _collect_states(lantern)

    assert states == [(True, '#000000')]


def test_small_color():
    with mock_serve([CHANGE_BYTES(1, 1, 1)]) as lantern:
        states = _collect_states(lantern)

    assert states == [(False, '#010101')]
