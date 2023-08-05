# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import curses
import sys
from typing import Any, Optional, Tuple, Union

from squirrelbattle.display.texturepack import TexturePack
from squirrelbattle.game import Game
from squirrelbattle.tests.screen import FakePad


class Display:
    x: int
    y: int
    width: int
    height: int
    pad: Any

    _color_pairs = {(curses.COLOR_WHITE, curses.COLOR_BLACK): 0}
    _colors_rgb = {}

    def __init__(self, screen: Any, pack: Optional[TexturePack] = None):
        self.screen = screen
        self.pack = pack or TexturePack.get_pack("ascii")

    def newpad(self, height: int, width: int) -> Union[FakePad, Any]:
        """
        Overwrites the native curses function of the same name.
        """
        return curses.newpad(height, width) if self.screen else FakePad()

    def truncate(self, msg: str, height: int, width: int) -> str:
        """
        Truncates a string into a string adapted to the width and height of
        the screen.
        """
        height = max(0, height)
        width = max(0, width)
        lines = msg.split("\n")
        lines = lines[:height]
        lines = [line[:width] for line in lines]
        return "\n".join(lines)

    def translate_color(self, color: Union[int, Tuple[int, int, int]]) -> int:
        """
        Translates a tuple (R, G, B) into a curses color index.
        If we already have a color index, then nothing is processed.
        If this is a tuple, we construct a new color index if non-existing
        and we return this index.
        The values of R, G and B must be between 0 and 1000, and not
        between 0 and 255.
        """
        if isinstance(color, tuple):
            # The color is a tuple (R, G, B), that is potentially unknown.
            # We translate it into a curses color number.
            if color not in self._colors_rgb:
                # The color does not exist, we create it.
                color_nb = len(self._colors_rgb) + 8
                self.init_color(color_nb, color[0], color[1], color[2])
                self._colors_rgb[color] = color_nb
            color = self._colors_rgb[color]
        return color

    def addstr(self, pad: Any, y: int, x: int, msg: str,
               fg_color: Union[int, Tuple[int, int, int]] = curses.COLOR_WHITE,
               bg_color: Union[int, Tuple[int, int, int]] = curses.COLOR_BLACK,
               *, altcharset: bool = False, blink: bool = False,
               bold: bool = False, dim: bool = False, invis: bool = False,
               italic: bool = False, normal: bool = False,
               protect: bool = False, reverse: bool = False,
               standout: bool = False, underline: bool = False,
               horizontal: bool = False, left: bool = False,
               low: bool = False, right: bool = False, top: bool = False,
               vertical: bool = False, chartext: bool = False) -> None:
        """
        Displays a message onto the pad.
        If the message is too large, it is truncated vertically and horizontally
        The text can be bold, italic, blinking, ... if the right parameters are
        given. These parameters are translated into curses attributes.
        The foreground and background colors can be given as curses constants
        (curses.COLOR_*), or by giving a tuple (R, G, B) that corresponds to
        the color. R, G, B must be between 0 and 1000, and not 0 and 255.
        """
        height, width = pad.getmaxyx()
        # Truncate message if it is too large
        msg = self.truncate(msg, height - y, width - x - 1)
        if msg.replace("\n", "") and x >= 0 and y >= 0:
            fg_color = self.translate_color(fg_color)
            bg_color = self.translate_color(bg_color)

            # Get the pair number for the tuple (fg, bg)
            # If it does not exist, create it and give a new unique id.
            if (fg_color, bg_color) in self._color_pairs:
                pair_nb = self._color_pairs[(fg_color, bg_color)]
            else:
                pair_nb = len(self._color_pairs)
                self.init_pair(pair_nb, fg_color, bg_color)
                self._color_pairs[(fg_color, bg_color)] = pair_nb

            # Compute curses attributes from the parameters
            attr = self.color_pair(pair_nb)
            attr |= curses.A_ALTCHARSET if altcharset else 0
            attr |= curses.A_BLINK if blink else 0
            attr |= curses.A_BOLD if bold else 0
            attr |= curses.A_DIM if dim else 0
            attr |= curses.A_INVIS if invis else 0
            # Italic is supported since Python 3.7
            italic &= sys.version_info >= (3, 7,)
            attr |= curses.A_ITALIC if italic else 0
            attr |= curses.A_NORMAL if normal else 0
            attr |= curses.A_PROTECT if protect else 0
            attr |= curses.A_REVERSE if reverse else 0
            attr |= curses.A_STANDOUT if standout else 0
            attr |= curses.A_UNDERLINE if underline else 0
            attr |= curses.A_HORIZONTAL if horizontal else 0
            attr |= curses.A_LEFT if left else 0
            attr |= curses.A_LOW if low else 0
            attr |= curses.A_RIGHT if right else 0
            attr |= curses.A_TOP if top else 0
            attr |= curses.A_VERTICAL if vertical else 0
            attr |= curses.A_CHARTEXT if chartext else 0

            return pad.addstr(y, x, msg, attr)

    def init_pair(self, number: int, foreground: int, background: int) -> None:
        foreground = foreground if self.screen and curses.can_change_color() \
            and foreground < curses.COLORS \
            else curses.COLOR_WHITE
        background = background if self.screen and curses.can_change_color() \
            and background < curses.COLORS \
            else curses.COLOR_WHITE
        return curses.init_pair(number, foreground, background) \
            if self.screen and curses.can_change_color() \
            and number < curses.COLOR_PAIRS else None

    def color_pair(self, number: int) -> int:
        return curses.color_pair(number) if self.screen \
            and number < curses.COLOR_PAIRS else 0

    def init_color(self, number: int, red: int, green: int, blue: int) -> None:
        return curses.init_color(number, red, green, blue) \
            if self.screen and curses.can_change_color() \
            and number < curses.COLORS else None

    def resize(self, y: int, x: int, height: int, width: int,
               resize_pad: bool = True) -> None:
        """
        Resizes a pad.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if hasattr(self, "pad") and resize_pad and \
                self.height >= 0 and self.width >= 0:
            self.pad.erase()
            self.pad.resize(self.height + 1, self.width + 1)

    def refresh(self, *args, resize_pad: bool = True) -> None:
        """
        Refreshes a pad
        """
        if len(args) == 4:
            self.resize(*args, resize_pad)
        self.display()

    def refresh_pad(self, pad: Any, top_y: int, top_x: int,
                    window_y: int, window_x: int,
                    last_y: int, last_x: int) -> None:
        """
        Refreshes a pad on a part of the window.
        The refresh starts at coordinates (top_y, top_x) from the pad,
        and is drawn from (window_y, window_x) to (last_y, last_x).
        If coordinates are invalid (negative indexes/length...), then nothing
        is drawn and no error is raised.
        """
        top_y, top_x = max(0, top_y), max(0, top_x)
        window_y, window_x = max(0, window_y), max(0, window_x)
        screen_max_y, screen_max_x = self.screen.getmaxyx() if self.screen \
            else (42, 42)
        last_y, last_x = min(screen_max_y - 1, last_y), \
            min(screen_max_x - 1, last_x)

        if last_y >= window_y and last_x >= window_x:
            # Refresh the pad only if coordinates are valid
            pad.noutrefresh(top_y, top_x, window_y, window_x, last_y, last_x)

    def display(self) -> None:
        """
        Draw the content of the display and refresh pads.
        """
        raise NotImplementedError

    def update(self, game: Game) -> None:
        """
        The game state was updated.
        Indicate what to do with the new state.
        """
        raise NotImplementedError

    def handle_click(self, y: int, x: int, attr: int, game: Game) -> None:
        """
        A mouse click was performed on the coordinates (y, x) of the pad.
        Maybe it should do something.
        """

    @property
    def rows(self) -> int:
        return curses.LINES if self.screen else 42

    @property
    def cols(self) -> int:
        return curses.COLS if self.screen else 42


class VerticalSplit(Display):
    """
    A class to split the screen in two vertically with a pretty line.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pad = self.newpad(self.rows, 1)

    @property
    def width(self) -> int:
        return 1

    @width.setter
    def width(self, val: Any) -> None:
        pass

    def display(self) -> None:
        for i in range(self.height):
            self.addstr(self.pad, i, 0, "┃")
        self.refresh_pad(self.pad, 0, 0, self.y, self.x,
                         self.y + self.height - 1, self.x)


class HorizontalSplit(Display):
    """
    A class to split the screen in two horizontally with a pretty line.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pad = self.newpad(1, self.cols)

    @property
    def height(self) -> int:
        return 1

    @height.setter
    def height(self, val: Any) -> None:
        pass

    def display(self) -> None:
        for i in range(self.width):
            self.addstr(self.pad, 0, i, "━")
        self.refresh_pad(self.pad, 0, 0, self.y, self.x, self.y,
                         self.x + self.width - 1)


class Box(Display):
    """
    A class for pretty boxes to print menus and other content.
    """
    title: str = ""

    def update_title(self, title: str) -> None:
        self.title = title

    def __init__(self, *args, fg_border_color: Optional[int] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.pad = self.newpad(self.rows, self.cols)
        self.fg_border_color = fg_border_color or curses.COLOR_WHITE

    def display(self) -> None:
        self.addstr(self.pad, 0, 0, "┏" + "━" * (self.width - 2) + "┓",
                    self.fg_border_color)
        for i in range(1, self.height - 1):
            self.addstr(self.pad, i, 0, "┃", self.fg_border_color)
            self.addstr(self.pad, i, self.width - 1, "┃", self.fg_border_color)
        self.addstr(self.pad, self.height - 1, 0,
                    "┗" + "━" * (self.width - 2) + "┛", self.fg_border_color)

        if self.title:
            self.addstr(self.pad, 0, (self.width - len(self.title) - 8) // 2,
                        f" == {self.title} == ", curses.COLOR_GREEN,
                        italic=True, bold=True)

        self.refresh_pad(self.pad, 0, 0, self.y, self.x,
                         self.y + self.height - 1, self.x + self.width - 1)


class MessageDisplay(Display):
    """
    A class to handle the display of popup messages.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.box = Box(fg_border_color=curses.COLOR_RED, *args, **kwargs)
        self.message = ""
        self.pad = self.newpad(1, 1)

    def update(self, game: Game) -> None:
        self.message = game.message

    def display(self) -> None:
        self.box.refresh(self.y - 1, self.x - 2,
                         self.height + 2, self.width + 4)
        self.box.display()
        self.pad.erase()
        self.addstr(self.pad, 0, 0, self.message, bold=True)
        self.refresh_pad(self.pad, 0, 0, self.y, self.x,
                         self.height + self.y - 1,
                         self.width + self.x - 1)
