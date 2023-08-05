# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import curses

from .display import Display
from ..entities.items import Monocle
from ..entities.player import Player
from ..game import Game
from ..interfaces import FightingEntity, Logs, Map
from ..translations import gettext as _


class LogsDisplay(Display):
    """
    A class to handle the display of the logs.
    """

    logs: Logs

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.pad = self.newpad(self.rows, self.cols)

    def update(self, game: Game) -> None:
        self.logs = game.logs

    def display(self) -> None:
        messages = self.logs.messages[-self.height:]
        messages = messages[::-1]
        self.pad.erase()
        for i in range(min(self.height, len(messages))):
            self.addstr(self.pad, self.height - i - 1, self.x,
                        messages[i][:self.width])
        self.refresh_pad(self.pad, 0, 0, self.y, self.x,
                         self.y + self.height - 1, self.x + self.width - 1)


class MapDisplay(Display):
    """
    A class to handle the display of the map.
    """

    map: Map

    def __init__(self, *args):
        super().__init__(*args)

    def update(self, game: Game) -> None:
        self.map = game.map
        self.pad = self.newpad(self.map.height,
                               self.pack.tile_width * self.map.width + 1)

    def update_pad(self) -> None:
        for j in range(len(self.map.tiles)):
            for i in range(len(self.map.tiles[j])):
                if not self.map.seen_tiles[j][i]:
                    continue
                fg, bg = self.map.tiles[j][i].visible_color(self.pack) if \
                    self.map.visibility[j][i] else \
                    self.map.tiles[j][i].hidden_color(self.pack)
                self.addstr(self.pad, j, self.pack.tile_width * i,
                            self.map.tiles[j][i].char(self.pack), fg, bg)
        for e in self.map.entities:
            if self.map.visibility[e.y][e.x]:
                self.addstr(self.pad, e.y, self.pack.tile_width * e.x,
                            self.pack[e.name.upper()],
                            self.pack.entity_fg_color,
                            self.pack.entity_bg_color)

        # Display Path map for debug purposes
        # from squirrelbattle.entities.player import Player
        # players = [ p for p in self.map.entities if isinstance(p,Player) ]
        # player = players[0] if len(players) > 0 else None
        # if player:
        #     for x in range(self.map.width):
        #         for y in range(self.map.height):
        #             if (y,x) in player.paths:
        #                 deltay, deltax = (y - player.paths[(y, x)][0],
        #                     x - player.paths[(y, x)][1])
        #                 if (deltay, deltax) == (-1, 0):
        #                     character = '↓'
        #                 elif (deltay, deltax) == (1, 0):
        #                     character = '↑'
        #                 elif (deltay, deltax) == (0, -1):
        #                     character = '→'
        #                 else:
        #                     character = '←'
        #                 self.addstr(self.pad, y, self.pack.tile_width * x,
        #                     character, self.pack.tile_fg_color,
        #                     self.pack.tile_bg_color)

    def display(self) -> None:
        y, x = self.map.currenty, self.pack.tile_width * self.map.currentx
        deltay, deltax = (self.height // 2) + 1, (self.width // 2) + 1
        pminrow, pmincol = y - deltay, x - deltax
        sminrow, smincol = max(-pminrow, 0), max(-pmincol, 0)
        deltay, deltax = self.height - deltay, self.width - deltax
        smaxrow = self.map.height - (y + deltay) + self.height - 1
        smaxrow = min(smaxrow, self.height - 1)
        smaxcol = self.pack.tile_width * self.map.width - \
            (x + deltax) + self.width - 1

        # Wrap perfectly the map according to the width of the tiles
        pmincol = self.pack.tile_width * (pmincol // self.pack.tile_width)
        smincol = self.pack.tile_width * (smincol // self.pack.tile_width)
        smaxcol = self.pack.tile_width \
            * (smaxcol // self.pack.tile_width + 1) - 1

        smaxcol = min(smaxcol, self.width - 1)
        pminrow = max(0, min(self.map.height, pminrow))
        pmincol = max(0, min(self.pack.tile_width * self.map.width, pmincol))

        self.pad.erase()
        self.update_pad()
        self.refresh_pad(self.pad, pminrow, pmincol, sminrow, smincol, smaxrow,
                         smaxcol)


class StatsDisplay(Display):
    """
    A class to handle the display of the stats of the player.
    """
    game: Game
    player: Player

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pad = self.newpad(self.rows, self.cols)

    def update(self, game: Game) -> None:
        self.game = game
        self.player = game.player

    def update_pad(self) -> None:
        string2 = f"{_(self.player.name).capitalize()} " \
                  f"-- LVL {self.player.level} -- " \
                  f"FLOOR {-self.player.map.floor}\n" \
                  f"EXP {self.player.current_xp}/{self.player.max_xp}\n" \
                  f"HP {self.player.health}/{self.player.maxhealth}"
        self.addstr(self.pad, 0, 0, string2)
        string3 = f"STR {self.player.strength}\n" \
                  f"INT {self.player.intelligence}\n" \
                  f"CHR {self.player.charisma}\n" \
                  f"DEX {self.player.dexterity}\n" \
                  f"CON {self.player.constitution}\n" \
                  f"CRI {self.player.critical}%"
        self.addstr(self.pad, 3, 0, string3)

        inventory_str = _("Inventory:") + " "
        # Stack items by type instead of displaying each item
        item_types = [item.name for item in self.player.inventory]
        item_types.sort(key=item_types.count, reverse=True)
        printed_items = []
        for item in item_types:
            if item in printed_items:
                continue
            count = item_types.count(item)
            inventory_str += self.pack[item.upper()]
            if count > 1:
                inventory_str += f"x{count} "
            printed_items.append(item)
        self.addstr(self.pad, 9, 0, inventory_str)

        if self.player.equipped_main:
            self.addstr(self.pad, 10, 0,
                        _("Equipped main:") + " "
                        f"{self.pack[self.player.equipped_main.name.upper()]}")
        if self.player.equipped_secondary:
            self.addstr(self.pad, 11, 0,
                        _("Equipped secondary:") + " "
                        + self.pack[self.player.equipped_secondary
                                    .name.upper()])
        if self.player.equipped_armor:
            self.addstr(self.pad, 12, 0,
                        _("Equipped chestplate:") + " "
                        + self.pack[self.player.equipped_armor.name.upper()])
        if self.player.equipped_helmet:
            self.addstr(self.pad, 13, 0,
                        _("Equipped helmet:") + " "
                        + self.pack[self.player.equipped_helmet.name.upper()])

        self.addstr(self.pad, 14, 0, f"{self.pack.HAZELNUT} "
                                     f"x{self.player.hazel}")

        if self.player.dead:
            self.addstr(self.pad, 15, 0, _("YOU ARE DEAD"), curses.COLOR_RED,
                        bold=True, blink=True, standout=True)

        if self.player.map.tiles[self.player.y][self.player.x].is_ladder():
            msg = _("Use {key} to use the ladder") \
                .format(key=self.game.settings.KEY_LADDER.upper())
            self.addstr(self.pad, self.height - 2, 0, msg,
                        italic=True, reverse=True)

        self.update_entities_stats()

    def update_entities_stats(self) -> None:
        """
        Display information about a near entity if we have a monocle.
        """
        for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            for entity in self.player.map.find_entities(FightingEntity):
                if entity == self.player:
                    continue

                if entity.y == self.player.y + dy \
                        and entity.x == self.player.x + dx:
                    if entity.is_friendly():
                        msg = _("Move to the friendly entity to talk to it") \
                            if self.game.waiting_for_friendly_key else \
                            _("Use {key} then move to talk to the entity") \
                            .format(key=self.game.settings.KEY_CHAT.upper())
                        self.addstr(self.pad, self.height - 1, 0, msg,
                                    italic=True, reverse=True)

                    if isinstance(self.player.equipped_secondary, Monocle):
                        # Truth monocle
                        message = f"{entity.translated_name.capitalize()} " \
                                  f"{self.pack[entity.name.upper()]}\n" \
                                  f"STR {entity.strength}\n" \
                                  f"INT {entity.intelligence}\n" \
                                  f"CHR {entity.charisma}\n" \
                                  f"DEX {entity.dexterity}\n" \
                                  f"CON {entity.constitution}\n" \
                                  f"CRI {entity.critical}%"
                        self.addstr(self.pad, 17, 0, message)
                    # Only display one entity
                    break

    def display(self) -> None:
        self.pad.erase()
        self.update_pad()
        self.refresh_pad(self.pad, 0, 0, self.y, self.x,
                         self.y + self.height - 1, self.width + self.x - 1)
