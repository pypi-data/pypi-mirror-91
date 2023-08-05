# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import curses
from random import randint
from typing import List

from .display import Box, Display
from ..entities.player import Player
from ..enums import GameMode, KeyValues
from ..game import Game
from ..menus import ChestMenu, MainMenu, Menu, SettingsMenu, StoreMenu
from ..resources import ResourceManager
from ..translations import gettext as _


class MenuDisplay(Display):
    """
    A class to display the menu objects.
    """
    menu: Menu
    position: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menubox = Box(*args, **kwargs)

    def update_menu(self, menu: Menu) -> None:
        self.menu = menu

        # Menu values are printed in pad
        self.pad = self.newpad(self.trueheight, self.truewidth + 2)

    def update_pad(self) -> None:
        for i in range(self.trueheight):
            self.addstr(self.pad, i, 0, "   " + self.values[i])
        # set a marker on the selected line
        self.addstr(self.pad, self.menu.position, 0, " >")

    def display(self) -> None:
        cornery = 0 if self.height - 2 >= self.menu.position - 1 \
            else self.trueheight - self.height + 2 \
            if self.height - 2 >= self.trueheight - self.menu.position else 0

        # Menu box
        self.menubox.refresh(self.y, self.x, self.height, self.width)
        self.pad.erase()
        self.update_pad()
        self.refresh_pad(self.pad, cornery, 0, self.y + 1, self.x + 1,
                         self.height - 2 + self.y,
                         self.width - 2 + self.x)

    def handle_click(self, y: int, x: int, attr: int, game: Game) -> None:
        """
        We can select a menu item with the mouse.
        """
        self.menu.position = max(0, min(len(self.menu.values) - 1, y - 1))
        game.handle_key_pressed(KeyValues.ENTER)

    @property
    def truewidth(self) -> int:
        return max([len(str(a)) for a in self.values])

    @property
    def trueheight(self) -> int:
        return len(self.values)

    @property
    def preferred_width(self) -> int:
        return self.truewidth + 6

    @property
    def preferred_height(self) -> int:
        return self.trueheight + 2

    @property
    def values(self) -> List[str]:
        return [str(a) for a in self.menu.values]


class SettingsMenuDisplay(MenuDisplay):
    """
    A class to display specifically a settingsmenu object.
    """
    menu: SettingsMenu

    def update(self, game: Game) -> None:
        self.update_menu(game.settings_menu)

    @property
    def values(self) -> List[str]:
        return [_(a[1][1]) + (" : "
                + ("?" if self.menu.waiting_for_key
                    and a == self.menu.validate() else a[1][0]
                   .replace("\n", "\\n"))
            if a[1][0] else "") for a in self.menu.values]


class MainMenuDisplay(Display):
    """
    A class to display specifically a mainmenu object.
    """
    def __init__(self, menu: MainMenu, *args):
        super().__init__(*args)
        self.menu = menu

        with open(ResourceManager.get_asset_path("ascii_art-title.txt"), "r")\
             as file:
            self.title = file.read().split("\n")

        self.pad = self.newpad(max(self.rows, len(self.title) + 30),
                               max(len(self.title[0]) + 5, self.cols))

        self.fg_color = curses.COLOR_WHITE

        self.menudisplay = MenuDisplay(self.screen, self.pack)
        self.menudisplay.update_menu(self.menu)

    def display(self) -> None:
        for i in range(len(self.title)):
            self.addstr(self.pad, 4 + i, max(self.width // 2
                        - len(self.title[0]) // 2 - 1, 0), self.title[i],
                        self.fg_color)
        msg = _("Credits")
        self.addstr(self.pad, self.height - 1, self.width - 1 - len(msg), msg)
        self.refresh_pad(self.pad, 0, 0, self.y, self.x,
                         self.height + self.y - 1,
                         self.width + self.x - 1)
        menuwidth = min(self.menudisplay.preferred_width, self.width)
        menuy, menux = len(self.title) + 8, self.width // 2 - menuwidth // 2 - 1
        self.menudisplay.refresh(
            menuy, menux, min(self.menudisplay.preferred_height,
                              self.height - menuy), menuwidth)

    def update(self, game: Game) -> None:
        self.menudisplay.update_menu(game.main_menu)

    def handle_click(self, y: int, x: int, attr: int, game: Game) -> None:
        menuwidth = min(self.menudisplay.preferred_width, self.width)
        menuy, menux = len(self.title) + 8, self.width // 2 - menuwidth // 2 - 1
        menuheight = min(self.menudisplay.preferred_height, self.height - menuy)

        if menuy <= y < menuy + menuheight and menux <= x < menux + menuwidth:
            self.menudisplay.handle_click(y - menuy, x - menux, attr, game)

        if y <= len(self.title):
            self.fg_color = randint(0, 1000), randint(0, 1000), randint(0, 1000)

        if y == self.height - 1 and x >= self.width - 1 - len(_("Credits")):
            game.state = GameMode.CREDITS


class PlayerInventoryDisplay(MenuDisplay):
    """
    A class to handle the display of the player's inventory.
    """
    player: Player = None
    selected: bool = True
    store_mode: bool = False
    chest_mode: bool = False

    def update(self, game: Game) -> None:
        self.player = game.player
        self.update_menu(game.inventory_menu)
        game.inventory_menu.update_player(self.player)
        self.store_mode = game.state == GameMode.STORE
        self.chest_mode = game.state == GameMode.CHEST
        self.selected = game.state == GameMode.INVENTORY \
            or (self.store_mode and not game.is_in_store_menu)\
            or (self.chest_mode and not game.is_in_chest_menu)

    def update_pad(self) -> None:
        self.menubox.update_title(_("INVENTORY"))
        for i, item in enumerate(self.menu.values):
            rep = self.pack[item.name.upper()]
            selection = f"[{rep}]" if i == self.menu.position \
                and self.selected else f" {rep} "
            self.addstr(self.pad, i + 1, 0, selection
                        + " " + ("[E]" if item.equipped else "")
                        + item.translated_name.capitalize()
                        + (f" ({item.description})" if item.description else "")
                        + (": " + str(item.price) + " Hazels"
                           if self.store_mode else ""))

        if self.store_mode:
            price = f"{self.pack.HAZELNUT} {self.player.hazel} Hazels"
            width = len(price) + (self.pack.tile_width - 1)
            self.addstr(self.pad, self.height - 3, self.width - width - 2,
                        price, italic=True)

    @property
    def truewidth(self) -> int:
        return max(1, self.height if hasattr(self, "height") else 10)

    @property
    def trueheight(self) -> int:
        return 2 + super().trueheight

    def handle_click(self, y: int, x: int, attr: int, game: Game) -> None:
        """
        We can select a menu item with the mouse.
        """
        self.menu.position = max(0, min(len(self.menu.values) - 1, y - 2))
        game.is_in_store_menu = False
        game.handle_key_pressed(KeyValues.ENTER)


class StoreInventoryDisplay(MenuDisplay):
    """
    A class to handle the display of a merchant's inventory.
    """
    menu: StoreMenu
    selected: bool = False

    def update(self, game: Game) -> None:
        self.update_menu(game.store_menu)
        self.selected = game.is_in_store_menu

    def update_pad(self) -> None:
        self.menubox.update_title(_("STALL"))
        for i, item in enumerate(self.menu.values):
            rep = self.pack[item.name.upper()]
            selection = f"[{rep}]" if i == self.menu.position \
                and self.selected else f" {rep} "
            self.addstr(self.pad, i + 1, 0, selection
                        + " " + item.translated_name.capitalize()
                        + (f" ({item.description})" if item.description else "")
                        + ": " + str(item.price) + " Hazels")

        price = f"{self.pack.HAZELNUT} {self.menu.merchant.hazel} Hazels"
        width = len(price) + (self.pack.tile_width - 1)
        self.addstr(self.pad, self.height - 3, self.width - width - 2, price,
                    italic=True)

    @property
    def truewidth(self) -> int:
        return max(1, self.height if hasattr(self, "height") else 10)

    @property
    def trueheight(self) -> int:
        return 2 + super().trueheight

    def handle_click(self, y: int, x: int, attr: int, game: Game) -> None:
        """
        We can select a menu item with the mouse.
        """
        self.menu.position = max(0, min(len(self.menu.values) - 1, y - 2))
        game.is_in_store_menu = True
        game.handle_key_pressed(KeyValues.ENTER)


class ChestInventoryDisplay(MenuDisplay):
    """
    A class to handle the display of a merchant's inventory.
    """
    menu: ChestMenu
    selected: bool = False

    def update(self, game: Game) -> None:
        self.update_menu(game.chest_menu)
        self.selected = game.is_in_chest_menu

    def update_pad(self) -> None:
        self.menubox.update_title(_("CHEST"))
        for i, item in enumerate(self.menu.values):
            rep = self.pack[item.name.upper()]
            selection = f"[{rep}]" if i == self.menu.position \
                and self.selected else f" {rep} "
            self.addstr(self.pad, i + 1, 0, selection
                        + " " + item.translated_name.capitalize())

    @property
    def truewidth(self) -> int:
        return max(1, self.height if hasattr(self, "height") else 10)

    @property
    def trueheight(self) -> int:
        return 2 + super().trueheight

    def handle_click(self, y: int, x: int, attr: int, game: Game) -> None:
        """
        We can select a menu item with the mouse.
        """
        self.menu.position = max(0, min(len(self.menu.values) - 1, y - 2))
        game.is_in_chest_menu = True
        game.handle_key_pressed(KeyValues.ENTER)


class CreditsDisplay(Display):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = Box(*args, **kwargs)
        self.pad = self.newpad(1, 1)
        self.ascii_art_displayed = False

    def update(self, game: Game) -> None:
        return

    def display(self) -> None:
        self.box.refresh(self.y, self.x, self.height, self.width)
        self.box.display()
        self.pad.erase()

        messages = [
            _("Credits"),
            "",
            "Squirrel Battle",
            "",
            _("Developers:"),
            "Yohann \"ÿnérant\" D'ANELLO",
            "Mathilde \"eichhornchen\" DÉPRÉS",
            "Nicolas \"nicomarg\" MARGULIES",
            "Charles \"charsle\" PEYRAT",
            "",
            _("Translators:"),
            "Hugo \"ifugao\" JACOB (español)",
        ]

        for i, msg in enumerate(messages):
            self.addstr(self.pad, i + (self.height - len(messages)) // 2,
                        (self.width - len(msg)) // 2, msg,
                        bold=(i == 0), italic=(":" in msg))

        if self.ascii_art_displayed:
            self.display_ascii_art()

        self.refresh_pad(self.pad, 0, 0, self.y + 1, self.x + 1,
                         self.height + self.y - 2,
                         self.width + self.x - 2)

    def display_ascii_art(self) -> None:
        with open(ResourceManager.get_asset_path("ascii-art-ecureuil.txt"))\
                as f:
            ascii_art = f.read().split("\n")

        height, width = len(ascii_art), len(ascii_art[0])
        y_offset, x_offset = (self.height - height) // 2,\
                             (self.width - width) // 2

        for i, line in enumerate(ascii_art):
            for j, c in enumerate(line):
                bg_color = curses.COLOR_WHITE
                fg_color = curses.COLOR_BLACK
                bold = False
                if c == ' ':
                    bg_color = curses.COLOR_BLACK
                elif c == '━' or c == '┃' or c == '⋀':
                    bold = True
                    fg_color = curses.COLOR_WHITE
                    bg_color = curses.COLOR_BLACK
                elif c == '|':
                    bold = True  # c = '┃'
                    fg_color = (100, 700, 1000)
                    bg_color = curses.COLOR_BLACK
                elif c == '▓':
                    fg_color = (700, 300, 0)
                elif c == '▒':
                    fg_color = (700, 300, 0)
                    bg_color = curses.COLOR_BLACK
                elif c == '░':
                    fg_color = (350, 150, 0)
                elif c == '█':
                    fg_color = (0, 0, 0)
                    bg_color = curses.COLOR_BLACK
                elif c == '▬':
                    c = '█'
                    fg_color = (1000, 1000, 1000)
                    bg_color = curses.COLOR_BLACK
                self.addstr(self.pad, y_offset + i, x_offset + j, c,
                            fg_color, bg_color, bold=bold)

    def handle_click(self, y: int, x: int, attr: int, game: Game) -> None:
        if self.pad.inch(y - 1, x - 1) != ord(" "):
            self.ascii_art_displayed = True
