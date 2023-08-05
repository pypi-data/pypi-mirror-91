# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import curses
from typing import Any, List

from .display import Display, HorizontalSplit, MessageDisplay, VerticalSplit
from .gamedisplay import LogsDisplay, MapDisplay, StatsDisplay
from .menudisplay import ChestInventoryDisplay, CreditsDisplay, \
    MainMenuDisplay, PlayerInventoryDisplay, \
    SettingsMenuDisplay, StoreInventoryDisplay
from .texturepack import TexturePack
from ..enums import DisplayActions
from ..game import Game, GameMode


class DisplayManager:

    def __init__(self, screen: Any, g: Game):
        self.game = g
        self.screen = screen
        pack = TexturePack.get_pack(self.game.settings.TEXTURE_PACK)
        self.mapdisplay = MapDisplay(screen, pack)
        self.statsdisplay = StatsDisplay(screen, pack)
        self.logsdisplay = LogsDisplay(screen, pack)
        self.playerinventorydisplay = PlayerInventoryDisplay(screen, pack)
        self.storeinventorydisplay = StoreInventoryDisplay(screen, pack)
        self.chestinventorydisplay = ChestInventoryDisplay(screen, pack)
        self.mainmenudisplay = MainMenuDisplay(self.game.main_menu,
                                               screen, pack)
        self.settingsmenudisplay = SettingsMenuDisplay(screen, pack)
        self.messagedisplay = MessageDisplay(screen, pack)
        self.hbar = HorizontalSplit(screen, pack)
        self.vbar = VerticalSplit(screen, pack)
        self.creditsdisplay = CreditsDisplay(screen, pack)
        self.displays = [self.statsdisplay, self.mapdisplay,
                         self.mainmenudisplay, self.settingsmenudisplay,
                         self.logsdisplay, self.messagedisplay,
                         self.playerinventorydisplay,
                         self.storeinventorydisplay, self.creditsdisplay,
                         self.chestinventorydisplay]
        self.update_game_components()

    def handle_display_action(self, action: DisplayActions, *params) -> None:
        """
        Handles the differents values of display action.
        """
        if action == DisplayActions.REFRESH:
            self.refresh()
        elif action == DisplayActions.UPDATE:
            self.update_game_components()
        elif action == DisplayActions.MOUSE:
            self.handle_mouse_click(*params)

    def update_game_components(self) -> None:
        """
        The game state was updated.
        Trigger all displays of these modifications.
        """
        for d in self.displays:
            d.pack = TexturePack.get_pack(self.game.settings.TEXTURE_PACK)
            d.update(self.game)

    def handle_mouse_click(self, y: int, x: int, attr: int) -> None:
        """
        Handles the mouse clicks.
        """
        displays = self.refresh()
        display = None
        for d in displays:
            top_y, top_x, height, width = d.y, d.x, d.height, d.width
            if top_y <= y < top_y + height and top_x <= x < top_x + width:
                # The click coordinates correspond to the coordinates
                # of that display
                display = d
        if display:
            display.handle_click(y - display.y, x - display.x, attr, self.game)

    def refresh(self) -> List[Display]:
        """
        Refreshes all components on the screen.
        """
        displays = []
        pack = TexturePack.get_pack(self.game.settings.TEXTURE_PACK)

        if self.game.state == GameMode.PLAY \
                or self.game.state == GameMode.INVENTORY \
                or self.game.state == GameMode.STORE\
                or self.game.state == GameMode.CHEST:
            # The map pad has already the good size
            self.mapdisplay.refresh(0, 0, self.rows * 4 // 5,
                                    self.mapdisplay.pack.tile_width
                                    * (self.cols * 4 // 5
                                       // self.mapdisplay.pack.tile_width),
                                    resize_pad=False)
            self.statsdisplay.refresh(0, self.cols * 4 // 5 + 1,
                                      self.rows, self.cols // 5 - 1)
            self.logsdisplay.refresh(self.rows * 4 // 5 + 1, 0,
                                     self.rows // 5 - 1, self.cols * 4 // 5)
            self.hbar.refresh(self.rows * 4 // 5, 0, 1, self.cols * 4 // 5)
            self.vbar.refresh(0, self.cols * 4 // 5, self.rows, 1)

            displays += [self.mapdisplay, self.statsdisplay, self.logsdisplay,
                         self.hbar, self.vbar]

            if self.game.state == GameMode.INVENTORY:
                self.playerinventorydisplay.refresh(
                    self.rows // 10,
                    pack.tile_width * (self.cols // (2 * pack.tile_width)),
                    8 * self.rows // 10,
                    pack.tile_width * (2 * self.cols // (5 * pack.tile_width)))
                displays.append(self.playerinventorydisplay)
            elif self.game.state == GameMode.STORE:
                self.storeinventorydisplay.refresh(
                    self.rows // 10,
                    pack.tile_width * (self.cols // (2 * pack.tile_width)),
                    8 * self.rows // 10,
                    pack.tile_width * (2 * self.cols // (5 * pack.tile_width)))
                self.playerinventorydisplay.refresh(
                    self.rows // 10,
                    pack.tile_width * (self.cols // (10 * pack.tile_width)),
                    8 * self.rows // 10,
                    pack.tile_width * (2 * self.cols // (5 * pack.tile_width)))
                displays.append(self.storeinventorydisplay)
                displays.append(self.playerinventorydisplay)
            elif self.game.state == GameMode.CHEST:
                self.chestinventorydisplay.refresh(
                    self.rows // 10,
                    pack.tile_width * (self.cols // (2 * pack.tile_width)),
                    8 * self.rows // 10,
                    pack.tile_width * (2 * self.cols // (5 * pack.tile_width)))
                self.playerinventorydisplay.refresh(
                    self.rows // 10,
                    pack.tile_width * (self.cols // (10 * pack.tile_width)),
                    8 * self.rows // 10,
                    pack.tile_width * (2 * self.cols // (5 * pack.tile_width)))
                displays.append(self.chestinventorydisplay)
                displays.append(self.playerinventorydisplay)
        elif self.game.state == GameMode.MAINMENU:
            self.mainmenudisplay.refresh(0, 0, self.rows, self.cols)
            displays.append(self.mainmenudisplay)
        elif self.game.state == GameMode.SETTINGS:
            self.settingsmenudisplay.refresh(0, 0, self.rows, self.cols)
            displays.append(self.settingsmenudisplay)
        elif self.game.state == GameMode.CREDITS:
            self.creditsdisplay.refresh(0, 0, self.rows, self.cols)
            displays.append(self.creditsdisplay)

        if self.game.message:
            height, width = 0, 0
            for line in self.game.message.split("\n"):
                height += 1
                width = max(width, len(line))
            y = pack.tile_width * (self.rows - height) // (2 * pack.tile_width)
            x = pack.tile_width * ((self.cols - width) // (2 * pack.tile_width))
            self.messagedisplay.refresh(y, x, height, width)
            displays.append(self.messagedisplay)

        self.resize_window()

        return displays

    def resize_window(self) -> bool:
        """
        When the window is resized, ensures that the screen size is updated.
        """
        y, x = self.screen.getmaxyx() if self.screen else (0, 0)
        if self.screen and curses.is_term_resized(self.rows,
                                                  self.cols):  # pragma: nocover
            curses.resizeterm(y, x)
            return True
        return False

    @property
    def rows(self) -> int:
        """
        Overwrites the native curses attribute of the same name,
        for testing purposes.
        """
        return curses.LINES if self.screen else 42

    @property
    def cols(self) -> int:
        """
        Overwrites the native curses attribute of the same name,
        for testing purposes.
        """
        return curses.COLS if self.screen else 42
