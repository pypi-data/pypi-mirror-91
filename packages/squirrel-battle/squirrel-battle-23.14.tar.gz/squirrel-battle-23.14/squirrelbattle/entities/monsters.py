# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

from random import shuffle

from .player import Player
from ..interfaces import FightingEntity, Map


class Monster(FightingEntity):
    """
    The class for all monsters in the dungeon.
    All specific monster classes overwrite this class,
    and the parameters are given in the __init__ function.
    An example of the specification of a monster that has a strength of 4
    and 20 max HP:

    class MyMonster(Monster):
        def __init__(self, strength: int = 4, maxhealth: int = 20,
                     *args, **kwargs) -> None:
            super().__init__(name="my_monster", strength=strength,
                             maxhealth=maxhealth, *args, **kwargs)

    With that way, attributes can be overwritten when the entity is created.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def act(self, m: Map) -> None:
        """
        By default, a monster will move randomly where it is possible
        If the player is closeby, the monster runs to the player.
        """
        super().act(m)
        target = None
        for entity in m.entities:
            if self.distance_squared(entity) <= 25 and \
                    isinstance(entity, Player):
                target = entity
                break

        # Monsters move according to a Dijkstra algorithm
        # that targets the player.
        # If they can not move and are already close to the player,
        # they hit.
        if target and (self.y, self.x) in target.paths and \
                self.map.is_visible_from(self.y, self.x,
                                         target.y, target.x, 5):
            # Moves to target player by choosing the best available path
            for next_y, next_x in target.paths[(self.y, self.x)]:
                moved = self.check_move(next_y, next_x, True)
                if moved:
                    break
                if self.distance_squared(target) <= 1:
                    self.map.logs.add_message(self.hit(target))
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

    def move(self, y: int, x: int) -> None:
        """
        Overwrites the move function to recalculate paths.
        """
        super().move(y, x)
        self.recalculate_paths()


class Tiger(Monster):
    """
    A tiger monster.
    """
    def __init__(self, name: str = "tiger", strength: int = 5,
                 maxhealth: int = 30, *args, **kwargs) -> None:
        super().__init__(name=name, strength=strength,
                         maxhealth=maxhealth, *args, **kwargs)


class Hedgehog(Monster):
    """
    A really mean hedgehog monster.
    """
    def __init__(self, name: str = "hedgehog", strength: int = 3,
                 maxhealth: int = 10, *args, **kwargs) -> None:
        super().__init__(name=name, strength=strength,
                         maxhealth=maxhealth, *args, **kwargs)


class Rabbit(Monster):
    """
    A rabbit monster.
    """
    def __init__(self, name: str = "rabbit", strength: int = 1,
                 maxhealth: int = 20, critical: int = 30,
                 *args, **kwargs) -> None:
        super().__init__(name=name, strength=strength,
                         maxhealth=maxhealth, critical=critical,
                         *args, **kwargs)


class TeddyBear(Monster):
    """
    A cute teddybear monster.
    """
    def __init__(self, name: str = "teddy_bear", strength: int = 0,
                 maxhealth: int = 50, *args, **kwargs) -> None:
        super().__init__(name=name, strength=strength,
                         maxhealth=maxhealth, *args, **kwargs)


class GiantSeaEagle(Monster):
    """
    An eagle boss
    """
    def __init__(self, name: str = "eagle", strength: int = 1000,
                 maxhealth: int = 5000, *args, **kwargs) -> None:
        super().__init__(name=name, strength=strength,
                         maxhealth=maxhealth, *args, **kwargs)
