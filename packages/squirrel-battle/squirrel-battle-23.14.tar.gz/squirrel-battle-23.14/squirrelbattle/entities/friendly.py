# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

from random import choice, shuffle

from .items import Bomb, Item
from .monsters import Monster
from .player import Player
from ..interfaces import Entity, FightingEntity, FriendlyEntity, \
    InventoryHolder, Map
from ..translations import gettext as _


class Merchant(InventoryHolder, FriendlyEntity):
    """
    The class of merchants in the dungeon.
    """
    def keys(self) -> list:
        """
        Returns a friendly entitie's specific attributes.
        """
        return super().keys() + ["inventory", "hazel"]

    def __init__(self, name: str = "merchant", inventory: list = None,
                 hazel: int = 75, maxhealth: int = 8, *args, **kwargs):
        super().__init__(name=name, maxhealth=maxhealth, *args, **kwargs)
        self.inventory = self.translate_inventory(inventory) \
            if inventory is not None else None
        self.hazel = hazel
        if self.inventory is None:
            self.inventory = []
            for i in range(5):
                self.inventory.append(choice(Item.get_all_items())())

    def talk_to(self, player: Player) -> str:
        """
        This function is used to open the merchant's inventory in a menu,
        and allows the player to buy/sell objects.
        """
        return _("I don't sell any squirrel")

    def change_hazel_balance(self, hz: int) -> None:
        """
        Changes the number of hazel the merchant has by hz.
        """
        self.hazel += hz


class Chest(InventoryHolder, FriendlyEntity):
    """
    A class of chest inanimate entities which contain objects.
    """
    annihilated: bool

    def __init__(self, name: str = "chest", inventory: list = None,
                 hazel: int = 0, *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)
        self.hazel = hazel
        self.inventory = self.translate_inventory(inventory) \
            if inventory is not None else None
        self.annihilated = False
        if self.inventory is None:
            self.inventory = []
            for i in range(3):
                self.inventory.append(choice(Item.get_all_items())())

    def talk_to(self, player: Player) -> str:
        """
        This function is used to open the chest's inventory in a menu,
        and allows the player to take objects.
        """
        return _("You have opened the chest")

    def take_damage(self, attacker: Entity, amount: int) -> str:
        """
        A chest is not living, it can not take damage
        """
        if isinstance(attacker, Bomb):
            self.die()
            self.annihilated = True
            return _("The chest exploded")
        return _("It's not really effective")

    @property
    def dead(self) -> bool:
        """
        Chest can not die
        """
        return self.annihilated


class Sunflower(FriendlyEntity):
    """
    A friendly sunflower.
    """
    def __init__(self, maxhealth: int = 20,
                 *args, **kwargs) -> None:
        super().__init__(name="sunflower", maxhealth=maxhealth, *args, **kwargs)

    @property
    def dialogue_option(self) -> list:
        """
        Lists all that a sunflower can say to the player.
        """
        return [_("Flower power!!"), _("The sun is warm today")]


class Familiar(FightingEntity):
    """
    A friendly familiar that helps the player defeat monsters.
    """
    def __init__(self, maxhealth: int = 25,
                 *args, **kwargs) -> None:
        super().__init__(maxhealth=maxhealth, *args, **kwargs)
        self.target = None

#    @property
#    def dialogue_option(self) -> list:
#        """
#        Debug function (to see if used in the real game)
#        """
#        return [_("My target is"+str(self.target))]

    def act(self, p: Player, m: Map) -> None:
        """
        By default, the familiar tries to stay at distance at most 2 of the
        player and if a monster comes in range 3, it focuses on the monster
        and attacks it.
        """
        if self.target is None:
            # If the previous target is dead(or if there was no previous target)
            # the familiar tries to get closer to the player.
            self.target = p
        elif self.target.dead:
            self.target = p
        if self.target == p:
            # Look for monsters around the player to kill TOFIX : if monster is
            # out of range, continue targetting player.
            for entity in m.entities:
                if (p.y - entity.y) ** 2 + (p.x - entity.x) ** 2 <= 9 and\
                        isinstance(entity, Monster):
                    self.target = entity
                    entity.paths = dict()  # Allows the paths to be calculated.
                    break

        # Familiars move according to a Dijkstra algorithm
        # that targets their target.
        # If they can not move and are already close to their target,
        # they hit, except if their target is the player.
        if self.target and (self.y, self.x) in self.target.paths:
            # Moves to target player by choosing the best available path
            for next_y, next_x in self.target.paths[(self.y, self.x)]:
                moved = self.check_move(next_y, next_x, True)
                if moved:
                    break
                if self.distance_squared(self.target) <= 1 and \
                        not isinstance(self.target, Player):
                    self.map.logs.add_message(self.hit(self.target))
                    break
        else:
            # Moves in a random direction
            # If the direction is not available, tries another one
            moves = [self.move_up, self.move_down,
                     self.move_left, self.move_right]
            shuffle(moves)
            for move in moves:
                if move():
                    break


class Trumpet(Familiar):
    """
    A class of familiars.
    """
    def __init__(self, name: str = "trumpet", strength: int = 3,
                 maxhealth: int = 30, *args, **kwargs) -> None:
        super().__init__(name=name, strength=strength,
                         maxhealth=maxhealth, *args, **kwargs)
