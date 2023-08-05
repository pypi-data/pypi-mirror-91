# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import curses
from types import TracebackType


class TermManager:  # pragma: no cover
    """
    The TermManager object initializes the terminal, returns a screen object and
    de-initializes the terminal after use.
    """
    def __init__(self):
        self.screen = curses.initscr()
        # convert escapes sequences to curses abstraction
        self.screen.keypad(True)
        # stop printing typed keys to the terminal
        curses.noecho()
        # send keys through without having to press <enter>
        curses.cbreak()
        # make cursor invisible
        curses.curs_set(False)
        # Catch mouse events
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        # Enable colors
        curses.start_color()

    def __enter__(self):
        return self

    def __exit__(self, exc_type: type, exc_value: Exception,
                 exc_traceback: TracebackType) -> None:
        # restore the terminal to its original state
        self.screen.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.curs_set(True)
        curses.endwin()
