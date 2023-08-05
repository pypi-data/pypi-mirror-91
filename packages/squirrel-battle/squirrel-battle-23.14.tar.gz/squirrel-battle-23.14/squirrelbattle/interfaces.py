# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

from copy import deepcopy
from enum import auto, Enum
from functools import reduce
from itertools import product
from math import ceil, sqrt
from queue import PriorityQueue
from random import choice, randint
from typing import Any, Dict, List, Optional, Tuple

from .display.texturepack import TexturePack
from .translations import gettext as _


class Logs:
    """
    The logs object stores the messages to display. It encapsulates a list
    of such messages, to allow multiple pointers to keep track of it even if
    the list was to be reassigned.
    """

    def __init__(self) -> None:
        self.messages = []

    def add_message(self, msg: str) -> None:
        self.messages.append(msg)

    def add_messages(self, msg: List[str]) -> None:
        self.messages += msg

    def clear(self) -> None:
        self.messages = []


class Slope():
    X: int
    Y: int

    def __init__(self, y: int, x: int) -> None:
        self.Y = y
        self.X = x

    def compare(self, other: "Slope") -> int:
        y, x = other.Y, other.X
        return self.Y * x - self.X * y

    def __lt__(self, other: "Slope") -> bool:
        return self.compare(other) < 0

    def __eq__(self, other: "Slope") -> bool:
        return self.compare(other) == 0

    def __gt__(self, other: "Slope") -> bool:
        return self.compare(other) > 0

    def __le__(self, other: "Slope") -> bool:
        return self.compare(other) <= 0

    def __ge__(self, other: "Slope") -> bool:
        return self.compare(other) >= 0


class Map:
    """
    The Map object represents a with its width, height
    and tiles, that have their custom properties.
    """
    floor: int
    width: int
    height: int
    start_y: int
    start_x: int
    tiles: List[List["Tile"]]
    visibility: List[List[bool]]
    seen_tiles: List[List[bool]]
    entities: List["Entity"]
    logs: Logs
    # coordinates of the point that should be
    # on the topleft corner of the screen
    currentx: int
    currenty: int

    def __init__(self, width: int = 0, height: int = 0, tiles: list = None,
                 start_y: int = 0, start_x: int = 0):
        self.floor = 0
        self.width = width
        self.height = height
        self.start_y = start_y
        self.start_x = start_x
        self.currenty = start_y
        self.currentx = start_x
        self.tiles = tiles or []
        self.visibility = [[False for _ in range(len(self.tiles[0]))]
                           for _ in range(len(self.tiles))]
        self.seen_tiles = [[False for _ in range(len(tiles[0]))]
                           for _ in range(len(self.tiles))]
        self.entities = []
        self.logs = Logs()

    def add_entity(self, entity: "Entity") -> None:
        """
        Registers a new entity in the map.
        """
        if entity.is_familiar():
            self.entities.insert(1, entity)
        else:
            self.entities.append(entity)
        entity.map = self

    def remove_entity(self, entity: "Entity") -> None:
        """
        Unregisters an entity from the map.
        """
        if entity in self.entities:
            self.entities.remove(entity)

    def find_entities(self, entity_class: type) -> list:
        return [entity for entity in self.entities
                if isinstance(entity, entity_class)]

    def is_free(self, y: int, x: int) -> bool:
        """
        Indicates that the tile at the coordinates (y, x) is empty.
        """
        return 0 <= y < self.height and 0 <= x < self.width and \
            self.tiles[y][x].can_walk() and \
            not any(entity.x == x and entity.y == y for entity in self.entities)

    def entity_is_present(self, y: int, x: int) -> bool:
        """
        Indicates that the tile at the coordinates (y, x) contains a killable
        entity.
        """
        return 0 <= y < self.height and 0 <= x < self.width and \
            any(entity.x == x and entity.y == y and entity.is_friendly()
                for entity in self.entities)

    @staticmethod
    def load(filename: str) -> "Map":
        """
        Reads a file that contains the content of a map,
        and builds a Map object.
        """
        with open(filename, "r") as f:
            file = f.read()
        return Map.load_from_string(file)

    @staticmethod
    def load_from_string(content: str) -> "Map":
        """
        Loads a map represented by its characters and builds a Map object.
        """
        lines = content.split("\n")
        first_line = lines[0]
        start_y, start_x = map(int, first_line.split(" "))
        lines = [line for line in lines[1:] if line]
        height = len(lines)
        width = len(lines[0])
        tiles = [[Tile.from_ascii_char(c)
                  for x, c in enumerate(line)] for y, line in enumerate(lines)]

        return Map(width, height, tiles, start_y, start_x)

    @staticmethod
    def load_dungeon_from_string(content: str) -> List[List["Tile"]]:
        """
        Transforms a string into the list of corresponding tiles.
        """
        lines = content.split("\n")
        tiles = [[Tile.from_ascii_char(c)
                  for x, c in enumerate(line)] for y, line in enumerate(lines)]
        return tiles

    def draw_string(self, pack: TexturePack) -> str:
        """
        Draws the current map as a string object that can be rendered
        in the window.
        """
        return "\n".join("".join(tile.char(pack) for tile in line)
                         for line in self.tiles)

    def is_visible_from(self, starty: int, startx: int, desty: int, destx: int,
                        max_range: int) -> bool:
        oldvisibility = deepcopy(self.visibility)
        oldseen = deepcopy(self.seen_tiles)
        self.compute_visibility(starty, startx, max_range)
        result = self.visibility[desty][destx]
        self.visibility = oldvisibility
        self.seen_tiles = oldseen
        return result

    def compute_visibility(self, y: int, x: int, max_range: int) -> None:
        """
        Sets the visible tiles to be the ones visible by an entity at point
        (y, x), using a twaked shadow casting algorithm
        """

        for line in self.visibility:
            for i in range(len(line)):
                line[i] = False
        self.set_visible(0, 0, 0, (y, x))
        for octant in range(8):
            self.compute_visibility_octant(octant, (y, x), max_range, 1,
                                           Slope(1, 1), Slope(0, 1))

    def crop_top_visibility(self, octant: int, origin: Tuple[int, int],
                            x: int, top: Slope) -> int:
        if top.X == 1:
            top_y = x
        else:
            top_y = ceil(((x * 2 - 1) * top.Y + top.X) / (top.X * 2))
            if self.is_wall(top_y, x, octant, origin):
                top_y += top >= Slope(top_y * 2 + 1, x * 2) and not \
                    self.is_wall(top_y + 1, x, octant, origin)
            else:
                ax = x * 2
                ax += self.is_wall(top_y + 1, x + 1, octant, origin)
                top_y += top > Slope(top_y * 2 + 1, ax)
        return top_y

    def crop_bottom_visibility(self, octant: int, origin: Tuple[int, int],
                               x: int, bottom: Slope) -> int:
        if bottom.Y == 0:
            bottom_y = 0
        else:
            bottom_y = ceil(((x * 2 - 1) * bottom.Y + bottom.X)
                            / (bottom.X * 2))
            bottom_y += bottom >= Slope(bottom_y * 2 + 1, x * 2) and \
                self.is_wall(bottom_y, x, octant, origin) and \
                not self.is_wall(bottom_y + 1, x, octant, origin)
        return bottom_y

    def compute_visibility_octant(self, octant: int, origin: Tuple[int, int],
                                  max_range: int, distance: int, top: Slope,
                                  bottom: Slope) -> None:
        for x in range(distance, max_range + 1):
            top_y = self.crop_top_visibility(octant, origin, x, top)
            bottom_y = self.crop_bottom_visibility(octant, origin, x, bottom)
            was_opaque = -1
            for y in range(top_y, bottom_y - 1, -1):
                if x + y > max_range:
                    continue
                is_opaque = self.is_wall(y, x, octant, origin)
                is_visible = is_opaque\
                    or ((y != top_y or top >= Slope(y, x))
                        and (y != bottom_y
                             or bottom <= Slope(y, x)))
                # is_visible = is_opaque\
                #     or ((y != top_y or top >= Slope(y, x))
                #         and (y != bottom_y or bottom <= Slope(y, x)))
                if is_visible:
                    self.set_visible(y, x, octant, origin)
                if x == max_range:
                    continue
                if is_opaque and was_opaque == 0:
                    nx, ny = x * 2, y * 2 + 1
                    nx -= self.is_wall(y + 1, x, octant, origin)
                    if top > Slope(ny, nx):
                        if y == bottom_y:
                            bottom = Slope(ny, nx)
                            break
                        else:
                            self.compute_visibility_octant(
                                octant, origin, max_range, x + 1, top,
                                Slope(ny, nx))
                    elif y == bottom_y:  # pragma: no cover
                        return
                elif not is_opaque and was_opaque == 1:
                    nx, ny = x * 2, y * 2 + 1
                    nx += self.is_wall(y + 1, x + 1, octant, origin)
                    if bottom >= Slope(ny, nx):  # pragma: no cover
                        return
                    top = Slope(ny, nx)
                was_opaque = is_opaque
            if was_opaque != 0:
                break

    @staticmethod
    def translate_coord(y: int, x: int, octant: int,
                        origin: Tuple[int, int]) -> Tuple[int, int]:
        ny, nx = origin
        if octant == 0:
            return ny - y, nx + x
        elif octant == 1:
            return ny - x, nx + y
        elif octant == 2:
            return ny - x, nx - y
        elif octant == 3:
            return ny - y, nx - x
        elif octant == 4:
            return ny + y, nx - x
        elif octant == 5:
            return ny + x, nx - y
        elif octant == 6:
            return ny + x, nx + y
        elif octant == 7:
            return ny + y, nx + x

    def is_wall(self, y: int, x: int, octant: int,
                origin: Tuple[int, int]) -> bool:
        y, x = self.translate_coord(y, x, octant, origin)
        return 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[0]) and \
            self.tiles[y][x].is_wall()

    def set_visible(self, y: int, x: int, octant: int,
                    origin: Tuple[int, int]) -> None:
        y, x = self.translate_coord(y, x, octant, origin)
        if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[0]):
            self.visibility[y][x] = True
            self.seen_tiles[y][x] = True

    def tick(self, p: Any) -> None:
        """
        Triggers all entity events.
        """
        for entity in self.entities:
            if entity.is_familiar():
                entity.act(p, self)
            else:
                entity.act(self)

    def save_state(self) -> dict:
        """
        Saves the map's attributes to a dictionary.
        """
        d = dict()
        d["width"] = self.width
        d["height"] = self.height
        d["start_y"] = self.start_y
        d["start_x"] = self.start_x
        d["currentx"] = self.currentx
        d["currenty"] = self.currenty
        d["entities"] = []
        for enti in self.entities:
            d["entities"].append(enti.save_state())
        d["map"] = self.draw_string(TexturePack.ASCII_PACK)
        d["seen_tiles"] = self.seen_tiles
        return d

    def load_state(self, d: dict) -> "Map":
        """
        Loads the map's attributes from a dictionary.
        """
        self.width = d["width"]
        self.height = d["height"]
        self.start_y = d["start_y"]
        self.start_x = d["start_x"]
        self.currentx = d["currentx"]
        self.currenty = d["currenty"]
        self.tiles = self.load_dungeon_from_string(d["map"])
        self.seen_tiles = d["seen_tiles"]
        self.visibility = [[False for _ in range(len(self.tiles[0]))]
                           for _ in range(len(self.tiles))]
        self.entities = []
        dictclasses = Entity.get_all_entity_classes_in_a_dict()
        for entisave in d["entities"]:
            self.add_entity(dictclasses[entisave["type"]](**entisave))

        return self

    @staticmethod
    def neighbourhood(grid: List[List["Tile"]], y: int, x: int,
                      large: bool = False, oob: bool = False) \
            -> List[List[int]]:
        """
        Returns up to 8 nearby coordinates, in a 3x3 square around the input
        coordinate if large is set to True, or in a 5-square cross by default.
        Does not return coordinates if they are out of bounds.
        """
        height, width = len(grid), len(grid[0])
        neighbours = []
        if large:
            dyxs = [[dy, dx] for dy, dx in product([-1, 0, 1], [-1, 0, 1])]
            dyxs = dyxs[:5] + dyxs[6:]
        else:
            dyxs = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        for dy, dx in dyxs:
            if oob or (0 <= y + dy < height and 0 <= x + dx < width):
                neighbours.append([y + dy, x + dx])
        return neighbours


class Tile(Enum):
    """
    The internal representation of the tiles of the map.
    """
    EMPTY = auto()
    WALL = auto()
    FLOOR = auto()
    LADDER = auto()
    DOOR = auto()

    @staticmethod
    def from_ascii_char(ch: str) -> "Tile":
        """
        Maps an ascii character to its equivalent in the texture pack.
        """
        for tile in Tile:
            if tile.char(TexturePack.ASCII_PACK) == ch:
                return tile
        raise ValueError(ch)

    def char(self, pack: TexturePack) -> str:
        """
        Translates a Tile to the corresponding character according
        to the texture pack.
        """
        val = getattr(pack, self.name)
        return val[0] if isinstance(val, tuple) else val

    def visible_color(self, pack: TexturePack) -> Tuple[int, int]:
        """
        Retrieve the tuple (fg_color, bg_color) of the current Tile
        if it is visible.
        """
        val = getattr(pack, self.name)
        return (val[2], val[4]) if isinstance(val, tuple) else \
            (pack.tile_fg_visible_color, pack.tile_bg_color)

    def hidden_color(self, pack: TexturePack) -> Tuple[int, int]:
        """
        Retrieve the tuple (fg_color, bg_color) of the current Tile.
        """
        val = getattr(pack, self.name)
        return (val[1], val[3]) if isinstance(val, tuple) else \
            (pack.tile_fg_color, pack.tile_bg_color)

    def is_wall(self) -> bool:
        """
        Is this Tile a wall?
        """
        return self == Tile.WALL or self == Tile.DOOR

    def is_ladder(self) -> bool:
        """
        Is this Tile a ladder?
        """
        return self == Tile.LADDER

    def can_walk(self) -> bool:
        """
        Checks if an entity (player or not) can move in this tile.
        """
        return not self.is_wall() and self != Tile.EMPTY


class Entity:
    """
    An Entity object represents any entity present on the map.
    """
    y: int
    x: int
    name: str
    map: Map
    paths: Dict[Tuple[int, int], Tuple[int, int]]

    # noinspection PyShadowingBuiltins
    def __init__(self, y: int = 0, x: int = 0, name: Optional[str] = None,
                 map: Optional[Map] = None, *ignored, **ignored2):
        self.y = y
        self.x = x
        self.name = name
        self.map = map
        self.paths = None

    def check_move(self, y: int, x: int, move_if_possible: bool = False)\
            -> bool:
        """
        Checks if moving to (y,x) is authorized.
        """
        free = self.map.is_free(y, x)
        if free and move_if_possible:
            self.move(y, x)
        return free

    def move(self, y: int, x: int) -> bool:
        """
        Moves an entity to (y,x) coordinates.
        """
        self.y = y
        self.x = x
        return True

    def move_up(self, force: bool = False) -> bool:
        """
        Moves the entity up one tile, if possible.
        """
        return self.move(self.y - 1, self.x) if force else \
            self.check_move(self.y - 1, self.x, True)

    def move_down(self, force: bool = False) -> bool:
        """
        Moves the entity down one tile, if possible.
        """
        return self.move(self.y + 1, self.x) if force else \
            self.check_move(self.y + 1, self.x, True)

    def move_left(self, force: bool = False) -> bool:
        """
        Moves the entity left one tile, if possible.
        """
        return self.move(self.y, self.x - 1) if force else \
            self.check_move(self.y, self.x - 1, True)

    def move_right(self, force: bool = False) -> bool:
        """
        Moves the entity right one tile, if possible.
        """
        return self.move(self.y, self.x + 1) if force else \
            self.check_move(self.y, self.x + 1, True)

    def recalculate_paths(self, max_distance: int = 12) -> None:
        """
        Uses Dijkstra algorithm to calculate best paths for other entities to
        go to this entity. If self.paths is None, does nothing.
        """
        if self.paths is None:
            return
        distances = []
        predecessors = []
        # four Dijkstras, one for each adjacent tile
        for dir_y, dir_x in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            queue = PriorityQueue()
            new_y, new_x = self.y + dir_y, self.x + dir_x
            if not 0 <= new_y < self.map.height or \
                    not 0 <= new_x < self.map.width or \
                    not self.map.tiles[new_y][new_x].can_walk():
                continue
            queue.put(((1, 0), (new_y, new_x)))
            visited = [(self.y, self.x)]
            distances.append({(self.y, self.x): (0, 0), (new_y, new_x): (1, 0)})
            predecessors.append({(new_y, new_x): (self.y, self.x)})
            while not queue.empty():
                dist, (y, x) = queue.get()
                if dist[0] >= max_distance or (y, x) in visited:
                    continue
                visited.append((y, x))
                for diff_y, diff_x in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    new_y, new_x = y + diff_y, x + diff_x
                    if not 0 <= new_y < self.map.height or \
                            not 0 <= new_x < self.map.width or \
                            not self.map.tiles[new_y][new_x].can_walk():
                        continue
                    new_distance = (dist[0] + 1,
                                    dist[1] + (not self.map.is_free(y, x)))
                    if not (new_y, new_x) in distances[-1] or \
                            distances[-1][(new_y, new_x)] > new_distance:
                        predecessors[-1][(new_y, new_x)] = (y, x)
                        distances[-1][(new_y, new_x)] = new_distance
                        queue.put((new_distance, (new_y, new_x)))
        # For each tile that is reached by at least one Dijkstra, sort the
        # different paths by distance to the player. For the technical bits :
        # The reduce function is a fold starting on the first element of the
        # iterable, and we associate the points to their distance, sort
        # along the distance, then only keep the points.
        self.paths = {}
        for y, x in reduce(set.union,
                           [set(p.keys()) for p in predecessors], set()):
            self.paths[(y, x)] = [p for d, p in sorted(
                [(distances[i][(y, x)], predecessors[i][(y, x)])
                 for i in range(len(distances)) if (y, x) in predecessors[i]])]

    def act(self, m: Map) -> None:
        """
        Defines the action the entity will do at each tick.
        By default, does nothing.
        """
        pass

    def distance_squared(self, other: "Entity") -> int:
        """
        Gives the square of the distance to another entity.
        Useful to check distances since taking the square root takes time.
        """
        return (self.y - other.y) ** 2 + (self.x - other.x) ** 2

    def distance(self, other: "Entity") -> float:
        """
        Gives the cartesian distance to another entity.
        """
        return sqrt(self.distance_squared(other))

    def is_fighting_entity(self) -> bool:
        """
        Is this entity a fighting entity?
        """
        return isinstance(self, FightingEntity)

    def is_item(self) -> bool:
        """
        Is this entity an item?
        """
        from squirrelbattle.entities.items import Item
        return isinstance(self, Item)

    def is_friendly(self) -> bool:
        """
        Is this entity a friendly entity?
        """
        return isinstance(self, FriendlyEntity)

    def is_familiar(self) -> bool:
        """
        Is this entity a familiar?
        """
        from squirrelbattle.entities.friendly import Familiar
        return isinstance(self, Familiar)

    def is_merchant(self) -> bool:
        """
        Is this entity a merchant?
        """
        from squirrelbattle.entities.friendly import Merchant
        return isinstance(self, Merchant)

    def is_chest(self) -> bool:
        """
        Is this entity a chest?
        """
        from squirrelbattle.entities.friendly import Chest
        return isinstance(self, Chest)

    @property
    def translated_name(self) -> str:
        """
        Translates the name of entities.
        """
        return _(self.name.replace("_", " "))

    @staticmethod
    def get_all_entity_classes() -> list:
        """
        Returns all entities subclasses.
        """
        from squirrelbattle.entities.items import BodySnatchPotion, Bomb, Heart
        from squirrelbattle.entities.monsters import Tiger, Hedgehog, \
            Rabbit, TeddyBear, GiantSeaEagle
        from squirrelbattle.entities.friendly import Merchant, Sunflower, \
            Trumpet, Chest
        return [BodySnatchPotion, Bomb, Chest, GiantSeaEagle, Heart,
                Hedgehog, Merchant, Rabbit, Sunflower, TeddyBear, Tiger,
                Trumpet]

    @staticmethod
    def get_weights() -> list:
        """
        Returns a weigth list associated to the above function, to
        be used to spawn random entities with a certain probability.
        """
        return [30, 80, 50, 1, 100, 100, 60, 70, 70, 20, 40, 40]

    @staticmethod
    def get_all_entity_classes_in_a_dict() -> dict:
        """
        Returns all entities subclasses in a dictionary.
        """
        from squirrelbattle.entities.player import Player
        from squirrelbattle.entities.monsters import Tiger, Hedgehog, Rabbit, \
            TeddyBear, GiantSeaEagle
        from squirrelbattle.entities.friendly import Merchant, Sunflower, \
            Trumpet, Chest
        from squirrelbattle.entities.items import BodySnatchPotion, Bomb, \
            Heart, Sword, Shield, Chestplate, Helmet, RingCritical, RingXP, \
            ScrollofDamage, ScrollofWeakening, Ruler, Bow, FireBallStaff, \
            Monocle
        return {
            "BodySnatchPotion": BodySnatchPotion,
            "Bomb": Bomb,
            "Bow": Bow,
            "Chest": Chest,
            "Chestplate": Chestplate,
            "FireBallStaff": FireBallStaff,
            "GiantSeaEagle": GiantSeaEagle,
            "Heart": Heart,
            "Hedgehog": Hedgehog,
            "Helmet": Helmet,
            "Merchant": Merchant,
            "Monocle": Monocle,
            "Player": Player,
            "Rabbit": Rabbit,
            "RingCritical": RingCritical,
            "RingXP": RingXP,
            "Ruler": Ruler,
            "ScrollofDamage": ScrollofDamage,
            "ScrollofWeakening": ScrollofWeakening,
            "Shield": Shield,
            "Sunflower": Sunflower,
            "Sword": Sword,
            "Trumpet": Trumpet,
            "TeddyBear": TeddyBear,
            "Tiger": Tiger,
        }

    def save_state(self) -> dict:
        """
        Saves the coordinates of the entity.
        """
        d = dict()
        d["x"] = self.x
        d["y"] = self.y
        d["type"] = self.__class__.__name__
        return d


class FightingEntity(Entity):
    """
    A FightingEntity is an entity that can fight, and thus has a health,
    level and stats.
    """
    maxhealth: int
    health: int
    strength: int
    intelligence: int
    charisma: int
    dexterity: int
    constitution: int
    level: int
    critical: int
    confused: int  # Seulement 0 ou 1

    def __init__(self, maxhealth: int = 0, health: Optional[int] = None,
                 strength: int = 0, intelligence: int = 0, charisma: int = 0,
                 dexterity: int = 0, constitution: int = 0, level: int = 0,
                 critical: int = 0, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.maxhealth = maxhealth
        self.health = maxhealth if health is None else health
        self.strength = strength
        self.intelligence = intelligence
        self.charisma = charisma
        self.dexterity = dexterity
        self.constitution = constitution
        self.level = level
        self.critical = critical
        self.effects = []  # effects = temporary buff or weakening of the stats.
        self.confused = 0

    @property
    def dead(self) -> bool:
        """
        Is this entity dead ?
        """
        return self.health <= 0

    def act(self, m: Map) -> None:
        """
        Refreshes all current effects.
        """
        for i in range(len(self.effects)):
            self.effects[i][2] -= 1

        copy = self.effects[:]
        for i in range(len(copy)):
            if copy[i][2] <= 0:
                setattr(self, copy[i][0],
                        getattr(self, copy[i][0]) - copy[i][1])
                self.effects.remove(copy[i])

    def hit(self, opponent: "FightingEntity") -> str:
        """
        The entity deals damage to the opponent
        based on their respective stats.
        """
        if self.confused:
            return _("{name} is confused, it can not hit {opponent}.")\
                .format(name=_(self.translated_name.capitalize()),
                        opponent=_(opponent.translated_name))
        diceroll = randint(1, 100)
        damage = max(0, self.strength)
        string = " "
        if diceroll <= self.critical:  # It is a critical hit
            damage *= 4
            string = " " + _("It's a critical hit!") + " "
        return _("{name} hits {opponent}.")\
            .format(name=_(self.translated_name.capitalize()),
                    opponent=_(opponent.translated_name)) + string + \
            opponent.take_damage(self, damage)

    def take_damage(self, attacker: "Entity", amount: int) -> str:
        """
        The entity takes damage from the attacker
        based on their respective stats.
        """
        damage = 0
        if amount != 0:
            damage = max(1, amount - self.constitution)
        self.health -= damage
        if self.health <= 0:
            self.die()
        return _("{name} takes {damage} damage.")\
            .format(name=self.translated_name.capitalize(), damage=str(damage))\
            + (" " + _("{name} dies.")
               .format(name=self.translated_name.capitalize())
               if self.health <= 0 else "")

    def die(self) -> None:
        """
        If a fighting entity has no more health, it dies and is removed.
        """
        self.map.remove_entity(self)

    def keys(self) -> list:
        """
        Returns a fighting entity's specific attributes.
        """
        return ["name", "maxhealth", "health", "level", "strength",
                "intelligence", "charisma", "dexterity", "constitution"]

    def save_state(self) -> dict:
        """
        Saves the state of the entity into a dictionary.
        """
        d = super().save_state()
        for name in self.keys():
            d[name] = getattr(self, name)
        return d


class FriendlyEntity(FightingEntity):
    """
    Friendly entities are living entities which do not attack the player.
    """
    dialogue_option: list

    def talk_to(self, player: Any) -> str:
        return _("{entity} said: {message}").format(
            entity=self.translated_name.capitalize(),
            message=choice(self.dialogue_option))

    def keys(self) -> list:
        """
        Returns a friendly entity's specific attributes.
        """
        return ["maxhealth", "health"]


class InventoryHolder(Entity):
    hazel: int  # Currency of the game
    inventory: list

    def translate_inventory(self, inventory: list) -> list:
        """
        Translates the JSON save of the inventory into a list of the items in
        the inventory.
        """
        for i in range(len(inventory)):
            if isinstance(inventory[i], dict):
                inventory[i] = self.dict_to_item(inventory[i])
                inventory[i].held_by = self
        return inventory

    def dict_to_item(self, item_dict: dict) -> Entity:
        """
        Translates a dictionnary that contains the state of an item
        into an item object.
        """
        entity_classes = self.get_all_entity_classes_in_a_dict()

        item_class = entity_classes[item_dict["type"]]
        return item_class(**item_dict)

    def save_state(self) -> dict:
        """
        The inventory of the merchant is saved in a JSON format.
        """
        d = super().save_state()
        d["hazel"] = self.hazel
        d["inventory"] = [item.save_state() for item in self.inventory]
        return d

    def add_to_inventory(self, obj: Any) -> None:
        """
        Adds an object to the inventory.
        """
        if obj not in self.inventory:
            self.inventory.append(obj)

    def remove_from_inventory(self, obj: Any) -> None:
        """
        Removes an object from the inventory.
        """
        if obj in self.inventory:
            self.inventory.remove(obj)

    def change_hazel_balance(self, hz: int) -> None:
        """
        Changes the number of hazel the entity has by hz. hz is negative
        when the entity loses money and positive when it gains money.
        """
        self.hazel += hz
