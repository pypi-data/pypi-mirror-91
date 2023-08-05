# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import auto, Enum
from typing import Optional

from squirrelbattle.settings import Settings

# This file contains a few useful enumeration classes used elsewhere in the code


class DisplayActions(Enum):
    """
    Display actions options for the callable displayaction Game uses
    It just calls the same action on the display object displayaction refers to.
    """
    REFRESH = auto()
    UPDATE = auto()
    MOUSE = auto()


class GameMode(Enum):
    """
    Game mode options.
    """
    MAINMENU = auto()
    PLAY = auto()
    SETTINGS = auto()
    INVENTORY = auto()
    STORE = auto()
    CHEST = auto()
    CREDITS = auto()


class KeyValues(Enum):
    """
    Key values options used in the game.
    """
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    ENTER = auto()
    INVENTORY = auto()
    USE = auto()
    EQUIP = auto()
    DROP = auto()
    SPACE = auto()
    CHAT = auto()
    WAIT = auto()
    LADDER = auto()
    LAUNCH = auto()
    DANCE = auto()

    @staticmethod
    def translate_key(key: str, settings: Settings) \
            -> Optional["KeyValues"]:  # noqa: C901
        """
        Translates the raw string key into an enum value that we can use.
        """
        if key in (settings.KEY_DOWN_SECONDARY,
                   settings.KEY_DOWN_PRIMARY):
            return KeyValues.DOWN
        elif key in (settings.KEY_LEFT_PRIMARY,
                     settings.KEY_LEFT_SECONDARY):
            return KeyValues.LEFT
        elif key in (settings.KEY_RIGHT_PRIMARY,
                     settings.KEY_RIGHT_SECONDARY):
            return KeyValues.RIGHT
        elif key in (settings.KEY_UP_PRIMARY,
                     settings.KEY_UP_SECONDARY):
            return KeyValues.UP
        elif key == settings.KEY_ENTER:
            return KeyValues.ENTER
        elif key == settings.KEY_INVENTORY:
            return KeyValues.INVENTORY
        elif key == settings.KEY_USE:
            return KeyValues.USE
        elif key == settings.KEY_EQUIP:
            return KeyValues.EQUIP
        elif key == settings.KEY_DROP:
            return KeyValues.DROP
        elif key == ' ':
            return KeyValues.SPACE
        elif key == settings.KEY_CHAT:
            return KeyValues.CHAT
        elif key == settings.KEY_WAIT:
            return KeyValues.WAIT
        elif key == settings.KEY_LADDER:
            return KeyValues.LADDER
        elif key == settings.KEY_LAUNCH:
            return KeyValues.LAUNCH
        elif key == settings.KEY_DANCE:
            return KeyValues.DANCE
