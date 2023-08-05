# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

from math import log
from random import randint
from typing import Dict, Optional, Tuple

from .items import Item
from ..interfaces import FightingEntity, InventoryHolder, Tile
from ..translations import gettext as _


class Player(InventoryHolder, FightingEntity):
    """
    The class of the player.
    """
    current_xp: int = 0
    max_xp: int = 10
    xp_buff: float = 1
    paths: Dict[Tuple[int, int], Tuple[int, int]]
    equipped_main: Optional[Item]
    equipped_secondary: Optional[Item]
    equipped_helmet: Optional[Item]
    equipped_armor: Optional[Item]

    def __init__(self, name: str = "player", maxhealth: int = 20,
                 strength: int = 5, intelligence: int = 1, charisma: int = 1,
                 dexterity: int = 1, constitution: int = 1, level: int = 1,
                 current_xp: int = 0, max_xp: int = 10, inventory: list = None,
                 hazel: int = 42, equipped_main: Optional[Item] = None,
                 equipped_armor: Optional[Item] = None, critical: int = 5,
                 equipped_secondary: Optional[Item] = None,
                 equipped_helmet: Optional[Item] = None, xp_buff: float = 1,
                 vision: int = 5, *args, **kwargs) -> None:
        super().__init__(name=name, maxhealth=maxhealth, strength=strength,
                         intelligence=intelligence, charisma=charisma,
                         dexterity=dexterity, constitution=constitution,
                         level=level, critical=critical, *args, **kwargs)
        self.current_xp = current_xp
        self.max_xp = max_xp
        self.xp_buff = xp_buff
        self.inventory = self.translate_inventory(inventory or [])
        self.paths = dict()
        self.hazel = hazel
        self.equipped_main = self.dict_to_item(equipped_main) \
            if isinstance(equipped_main, dict) else equipped_main
        self.equipped_armor = self.dict_to_item(equipped_armor) \
            if isinstance(equipped_armor, dict) else equipped_armor
        self.equipped_secondary = self.dict_to_item(equipped_secondary) \
            if isinstance(equipped_secondary, dict) else equipped_secondary
        self.equipped_helmet = self.dict_to_item(equipped_helmet) \
            if isinstance(equipped_helmet, dict) else equipped_helmet
        self.vision = vision

    def move(self, y: int, x: int) -> None:
        """
        Moves the view of the map (the point on which the camera is centered)
        according to the moves of the player.
        """
        super().move(y, x)
        self.map.currenty = y
        self.map.currentx = x
        self.recalculate_paths()
        self.map.compute_visibility(self.y, self.x, self.vision)

    def dance(self) -> None:
        """
        Dancing has a certain probability or making ennemies unable
        to fight for 3 turns. That probability depends on the player's
        charisma.
        """
        diceroll = randint(1, 10)
        found = False
        if diceroll <= self.charisma:
            for entity in self.map.entities:
                if entity.is_fighting_entity() and not entity == self \
                        and entity.distance(self) <= 3:
                    found = True
                    entity.confused = 1
                    entity.effects.append(["confused", 1, 3])
            if found:
                self.map.logs.add_message(_(
                    "It worked! Nearby ennemies will be confused for 3 turns."))
            else:
                self.map.logs.add_message(_(
                    "It worked, but there is no one nearby..."))
        else:
            self.map.logs.add_message(
                _("The dance was not effective..."))

    def level_up(self) -> None:
        """
        Add as many levels as possible to the player.
        """
        while self.current_xp > self.max_xp:
            self.level += 1
            self.current_xp -= self.max_xp
            self.max_xp = self.level * 10
            self.maxhealth += int(2 * log(self.level) / log(2))
            self.health = self.maxhealth
            self.strength = self.strength + 1
            if self.level % 3 == 0:
                self.dexterity += 1
                self.constitution += 1
            if self.level % 4 == 0:
                self.intelligence += 1
            if self.level % 6 == 0:
                self.charisma += 1
            if self.level % 10 == 0 and self.critical < 95:
                self.critical += (100 - self.charisma) // 30

    def add_xp(self, xp: int) -> None:
        """
        Adds some experience to the player.
        If the required amount is reached, the player levels up.
        """
        self.current_xp += int(xp * self.xp_buff)
        self.level_up()

    # noinspection PyTypeChecker,PyUnresolvedReferences
    def check_move(self, y: int, x: int, move_if_possible: bool = False) \
            -> bool:
        """
        If the player tries to move but a fighting entity is there,
        the player fights this entity.
        If the entity dies, the player is rewarded with some XP
        """
        # Don't move if we are dead
        if self.dead:
            return False
        for entity in self.map.entities:
            if entity.y == y and entity.x == x:
                if entity.is_fighting_entity():
                    self.map.logs.add_message(self.hit(entity))
                    if entity.dead:
                        self.add_xp(randint(3, 7))
                    return True
                elif entity.is_item():
                    entity.hold(self)
        tile = self.map.tiles[y][x]
        if tile == Tile.DOOR and move_if_possible:
            # Open door
            self.map.tiles[y][x] = Tile.FLOOR
            self.map.compute_visibility(y, x, self.vision)
            return super().check_move(y, x, move_if_possible)
        return super().check_move(y, x, move_if_possible)

    def save_state(self) -> dict:
        """
        Saves the state of the entity into a dictionary
        """
        d = super().save_state()
        d["current_xp"] = self.current_xp
        d["max_xp"] = self.max_xp
        d["equipped_main"] = self.equipped_main.save_state()\
            if self.equipped_main else None
        d["equipped_armor"] = self.equipped_armor.save_state()\
            if self.equipped_armor else None
        d["equipped_secondary"] = self.equipped_secondary.save_state()\
            if self.equipped_secondary else None
        d["equipped_helmet"] = self.equipped_helmet.save_state()\
            if self.equipped_helmet else None
        return d
