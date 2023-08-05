# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import locale
import os
from typing import Any, Generator

from .resources import ResourceManager
from .translations import gettext as _


class Settings:
    """
    This class stores the settings of the game.
    Settings can be obtained by using for example settings.TEXTURE_PACK
    directly.
    The comment can be obtained by using settings.get_comment('TEXTURE_PACK').
    We can set the setting by simply using settings.TEXTURE_PACK = 'new_key'
    """
    def __init__(self):
        self.KEY_UP_PRIMARY = ['z', 'Main key to move up']
        self.KEY_UP_SECONDARY = ['KEY_UP', 'Secondary key to move up']
        self.KEY_DOWN_PRIMARY = ['s', 'Main key to move down']
        self.KEY_DOWN_SECONDARY = ['KEY_DOWN', 'Secondary key to move down']
        self.KEY_LEFT_PRIMARY = ['q', 'Main key to move left']
        self.KEY_LEFT_SECONDARY = ['KEY_LEFT', 'Secondary key to move left']
        self.KEY_RIGHT_PRIMARY = ['d', 'Main key to move right']
        self.KEY_RIGHT_SECONDARY = ['KEY_RIGHT', 'Secondary key to move right']
        self.KEY_ENTER = ['\n', 'Key to validate a menu']
        self.KEY_INVENTORY = ['i', 'Key used to open the inventory']
        self.KEY_USE = ['u', 'Key used to use an item in the inventory']
        self.KEY_EQUIP = ['e', 'Key used to equip an item in the inventory']
        self.KEY_DROP = ['r', 'Key used to drop an item in the inventory']
        self.KEY_CHAT = ['t', 'Key used to talk to a friendly entity']
        self.KEY_WAIT = ['w', 'Key used to wait']
        self.KEY_LADDER = ['<', 'Key used to use ladders']
        self.KEY_LAUNCH = ['l', 'Key used to use a bow']
        self.KEY_DANCE = ['y', 'Key used to dance']
        self.TEXTURE_PACK = ['ascii', 'Texture pack']
        self.LOCALE = [locale.getlocale()[0][:2], 'Language']

    def __getattribute__(self, item: str) -> Any:
        superattribute = super().__getattribute__(item)
        if item.isupper() and item in self.settings_keys:
            return superattribute[0]
        return superattribute

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.settings_keys:
            object.__getattribute__(self, name)[0] = value
            return
        return super().__setattr__(name, value)

    def get_comment(self, item: str) -> str:
        """
        Retrieves the comment relative to a setting.
        """
        if item in self.settings_keys:
            return _(object.__getattribute__(self, item)[1])
        for key in self.settings_keys:
            if getattr(self, key) == item:
                return _(object.__getattribute__(self, key)[1])

    @property
    def settings_keys(self) -> Generator[str, Any, None]:
        """
        Gets the list of all parameters.
        """
        return (key for key in self.__dict__)

    def loads_from_string(self, json_str: str) -> None:
        """
        Loads settings.
        """
        d = json.loads(json_str)
        for key in d:
            if hasattr(self, key):
                setattr(self, key, d[key])

    def dumps_to_string(self) -> str:
        """
        Dumps settings.
        """
        d = dict()
        for key in self.settings_keys:
            d[key] = getattr(self, key)
        return json.dumps(d, indent=4)

    def load_settings(self) -> None:
        """
        Loads the settings from a file
        """
        file_path = ResourceManager.get_config_path("settings.json")
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                self.loads_from_string(f.read())

    def write_settings(self) -> None:
        """
        Dumps the settings into a file
        """
        with open(ResourceManager.get_config_path("settings.json"), "w") as f:
            f.write(self.dumps_to_string())
