# Copyright (C) 2020 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

from random import choice, choices, randint, random, shuffle
from typing import List, Tuple

from ..interfaces import Entity, Map, Tile

DEFAULT_PARAMS = {
    "width": 120,
    "height": 35,
    "tries": 300,
    "max_rooms": 20,
    "max_room_tries": 15,
    "cross_room": 1,
    "corridor_chance": .2,
    "min_v_corr": 2,
    "max_v_corr": 6,
    "min_h_corr": 4,
    "max_h_corr": 12,
    "large_circular_room": .10,
    "circular_holes": .5,
    "loop_tries": 40,
    "loop_max": 5,
    "loop_threshold": 15,
    "spawn_per_region": [1, 2],
    "room_chances": {
        "circular": 5,
        "chunks": 1,
    },
}


def dist(level: List[List[Tile]], y1: int, x1: int, y2: int, x2: int) -> int:
    """
    Compute the minimum walking distance between points (y1, x1) and (y2, x2)
    on a Tile grid
    """
    # simple breadth first search
    copy = [[t for t in row] for row in level]
    dist = -1
    queue, next_queue = [[y1, x1]], [0]
    while next_queue:
        next_queue = []
        dist += 1
        while queue:
            y, x = queue.pop()
            copy[y][x] = Tile.EMPTY
            if y == y2 and x == x2:
                return dist
            for y, x in Map.neighbourhood(copy, y, x):
                if copy[y][x].can_walk():
                    next_queue.append([y, x])
        queue = next_queue
    return -1


class Generator:
    def __init__(self, params: dict = None):
        self.params = params or DEFAULT_PARAMS
        self.spawn_areas = []
        self.queued_area = None

    @staticmethod
    def room_fits(level: List[List[Tile]], y: int, x: int,
                  room: List[List[Tile]], door_y: int, door_x: int,
                  dy: int, dx: int) -> bool:
        """
        Using point (door_y, door_x) in the room as a reference and placing it
        over point (y, x) in the level, returns whether or not the room fits
        here
        """
        lh, lw = len(level), len(level[0])
        rh, rw = len(room), len(room[0])
        if not(0 < y + dy < lh and 0 < x + dx < lw):
            return False
        # door must be placed on an empty tile, and point into a floor tile
        if level[y][x] != Tile.EMPTY or level[y + dy][x + dx] != Tile.FLOOR:
            return False
        # now we verify floor tiles in both grids do not overlap
        for ry in range(rh):
            for rx in range(rw):
                if room[ry][rx] == Tile.FLOOR:
                    ly, lx = y + ry - door_y, x + rx - door_x
                    # tile must be in bounds and empty
                    if not(0 <= ly < lh and 0 <= lx < lw) or \
                            level[ly][lx] == Tile.FLOOR:
                        return False
                    # so do all neighbouring tiles bc we may
                    # need to place walls there eventually
                    for ny, nx in Map.neighbourhood(level, ly, lx,
                                                    large=True, oob=True):
                        if not(0 <= ny < lh and 0 <= nx < lw) or \
                                level[ny][nx] != Tile.EMPTY:
                            return False
        return True

    @staticmethod
    def place_room(level: List[List[Tile]], y: int, x: int,
                   room: List[List[Tile]], door_y: int, door_x: int) -> None:
        """
        Mutates level in place to add the room. Placement is determined by
        making (door_y, door_x) in the room correspond with (y, x) in the level
        """
        rh, rw = len(room), len(room[0])
        level[y][x] = Tile.DOOR
        for ry in range(rh):
            for rx in range(rw):
                if room[ry][rx] == Tile.FLOOR:
                    level[y - door_y + ry][x - door_x + rx] = Tile.FLOOR

    @staticmethod
    def add_loop(level: List[List[Tile]], y: int, x: int) -> bool:
        """
        Try to add a corridor between two far apart floor tiles, passing
        through point (y, x).
        """
        h, w = len(level), len(level[0])

        if level[y][x] != Tile.EMPTY:
            return False

        # loop over both directions, trying to place both veritcal
        # and horizontal corridors
        for dx, dy in [[0, 1], [1, 0]]:
            # then we find two floor tiles, one on each side of (y, x)
            # exiting if we don't find two (reach the edge of the map before)
            y1, x1, y2, x2 = y, x, y, x
            while x1 >= 0 and y1 >= 0 and level[y1][x1] == Tile.EMPTY:
                y1, x1 = y1 - dy, x1 - dx
            while x2 < w and y2 < h and level[y2][x2] == Tile.EMPTY:
                y2, x2 = y2 + dy, x2 + dx
            if not(0 <= x1 <= x2 < w and 0 <= y1 <= y2 < h):
                continue

            def verify_sides() -> bool:
                # switching up dy and dx here pivots the axis, so
                # (y+dx, x+dy) and (y-dx, x-dy) are the tiles adjacent to
                # (y, x), but not on the original axis
                for delta_x, delta_y in [[dy, dx], [-dy, -dx]]:
                    for i in range(1, y2 - y1 + x2 - x1):
                        if not (0 <= y1 + delta_y + i * dy < h
                                and 0 <= x1 + delta_x + i * dx < w) or \
                                level[y1 + delta_y + i * dy][x1 + delta_x
                                                             + i * dx]\
                                .can_walk():
                            return False
                return True
            # if adding the path would make the two tiles significantly closer
            # and its sides don't touch already placed terrain, build it
            if dist(level, y1, x1, y2, x2) < 20 and verify_sides():
                y, x = y1 + dy, x1 + dx
                while level[y][x] == Tile.EMPTY:
                    level[y][x] = Tile.FLOOR
                    y, x = y + dy, x + dx
                return True
        return False

    @staticmethod
    def place_walls(level: List[List[Tile]]) -> None:
        """
        Place wall tiles on every empty tile that is adjacent (in the largest
        sense), to a floor tile
        """
        h, w = len(level), len(level[0])
        for y in range(h):
            for x in range(w):
                if not level[y][x].is_wall():
                    for ny, nx in Map.neighbourhood(level, y, x, large=True):
                        if level[ny][nx] == Tile.EMPTY:
                            level[ny][nx] = Tile.WALL

    def corr_meta_info(self) -> Tuple[int, int, int, int]:
        """
        Return info about the extra grid space that should be allocated for the
        room, and where the room should be built along this extra grid space.
        Because grids are usually thight around the room, this gives us extra
        place to add a corridor later. Corridor length and orientation is
        implicitly derived from this info.

        h_sup and w_sup represent the extra needed space along each axis,
        and h_off and w_off are the offset at which to build the room
        """
        if random() < self.params["corridor_chance"]:
            h_sup = randint(self.params["min_v_corr"],
                            self.params["max_v_corr"]) if random() < .5 else 0
            # we only allow extra space allocation along one axis,
            # because there won't more than one exit corridor
            w_sup = 0 if h_sup else randint(self.params["min_h_corr"],
                                            self.params["max_h_corr"])
            # implicitly choose which direction along the axis
            # the corridor will be pointing to
            h_off = h_sup if random() < .5 else 0
            w_off = w_sup if random() < .5 else 0
            return h_sup, w_sup, h_off, w_off
        return 0, 0, 0, 0

    @staticmethod
    def build_door(room: List[List[Tile]], y: int, x: int,
                   dy: int, dx: int, length: int) -> bool:
        """
        Tries to build the exit from the room at given coordinates
        Depending on parameter length, it will either attempt to build a
        simple door, or a long corridor.  Return value is a boolean
        signifying whether or not the exit was successfully built
        """
        rh, rw = len(room), len(room[0])
        # verify we are pointing away from a floor tile
        if not(0 <= y - dy < rh and 0 <= x - dx < rw) \
                or room[y - dy][x - dx] != Tile.FLOOR:
            return False
        # verify there's no other floor tile around us
        for ny, nx in [[y + dy, x + dx], [y - dx, x - dy],
                       [y + dx, x + dy]]:
            if 0 <= ny < rh and 0 <= nx < rw \
                    and room[ny][nx] != Tile.EMPTY:
                return False
        # see if the path ahead is clear. needed in the case of non convex room
        for i in range(length + 1):
            if room[y + i * dy][x + i * dx] != Tile.EMPTY:
                return False
        for i in range(length):
            room[y + i * dy][x + i * dx] = Tile.FLOOR
        return True

    @staticmethod
    def attach_door(room: List[List[Tile]], h_sup: int, w_sup: int,
                    h_off: int, w_off: int) -> Tuple[int, int, int, int]:
        """
        Attach an exit to the room. If extra space was allocated to
        the grid, make sure a corridor is properly built
        """
        length = h_sup + w_sup
        dy, dx = 0, 0
        if length > 0:
            if h_sup:
                dy = -1 if h_off else 1
            else:
                dx = -1 if w_off else 1
        else:
            # determine door direction for rooms without corridors
            if random() < .5:
                dy = -1 if random() < .5 else 1
            else:
                dx = -1 if random() < .5 else 1

        # loop over all possible positions in a random order
        rh, rw = len(room), len(room[0])
        yxs = [i for i in range(rh * rw)]
        shuffle(yxs)
        for pos in yxs:
            y, x = pos // rw, pos % rw
            if room[y][x] == Tile.EMPTY and \
                    Generator.build_door(room, y, x, dy, dx, length):
                break
        else:  # pragma: no cover
            return None, None, None, None

        return y + length * dy, x + length * dx, dy, dx

    def create_chunk_room(self, spawnable: bool = True) \
            -> Tuple[List[List[Tile]], int, int, int, int]:
        """
        Create and return as a tile grid a room that is composed of multiple
        overlapping circles of the same radius
        Also return door info so we know how to place the room in the level
        """
        height, width = 15, 15
        nb_chunks, r = 6, 3

        h_sup, w_sup, h_off, w_off = self.corr_meta_info()
        room = [[Tile.EMPTY] * (width + w_sup)
                for _dummy in range(height + h_sup)]

        def draw_chunk(room: List[List[Tile]], y: int, x: int) -> None:
            for i in range(y - r, y + r + 1):
                d = (y - i)**2
                for j in range(x - r, x + r + 1):
                    if d + (x - j) ** 2 < r ** 2:
                        room[i][j] = Tile.FLOOR

        draw_chunk(room, h_off + height // 2 + 1, w_off + width // 2 + 1)

        min_w, max_w = w_off + r + 1, width + w_off - r - 1
        min_h, max_h = h_off + r + 1, height + h_off - r - 1
        for i in range(nb_chunks):
            y, x = randint(min_h, max_h), randint(min_w, max_w)
            while room[y][x] != Tile.FLOOR:
                y, x = randint(min_h, max_h), randint(min_w, max_w)
            draw_chunk(room, y, x)

        # log all placed tiles as spawn positions
        if spawnable:
            self.register_spawn_area(room)

        # attach exit
        door_y, door_x, dy, dx = self.attach_door(room, h_sup, w_sup,
                                                  h_off, w_off)

        return room, door_y, door_x, dy, dx

    def create_circular_room(self, spawnable: bool = True) \
            -> Tuple[List[List[Tile]], int, int, int, int]:
        """
        Create and return as a tile grid a room that is circular in shape, and
        may have a center, also circular hole
        Also return door info so we know how to place the room in the level
        """
        if random() < self.params["large_circular_room"]:
            r = randint(5, 10)
        else:
            r = randint(2, 4)

        room = []

        h_sup, w_sup, h_off, w_off = self.corr_meta_info()

        height = 2 * r + 2
        width = 2 * r + 2
        make_hole = r > 6 and random() < self.params["circular_holes"]
        r2 = 0
        if make_hole:
            r2 = randint(3, r - 3)
        for i in range(height + h_sup):
            room.append([])
            d = (i - h_off - height // 2) ** 2
            for j in range(width + w_sup):
                if d + (j - w_off - width // 2) ** 2 < r ** 2 and \
                    (not make_hole
                     or d + (j - w_off - width // 2) ** 2 >= r2 ** 2):
                    room[-1].append(Tile.FLOOR)
                else:
                    room[-1].append(Tile.EMPTY)

        # log all placed tiles as spawn positions
        if spawnable:
            self.register_spawn_area(room)

        # attach exit
        door_y, door_x, dy, dx = self.attach_door(room, h_sup, w_sup,
                                                  h_off, w_off)

        return room, door_y, door_x, dy, dx

    def create_random_room(self, spawnable: bool = True) \
            -> Tuple[List[list], int, int, int, int]:
        """
        Randomly select a room shape and return one such room along with its
        door info. Set spawnable to False is the room should be marked as a
        potential spawning region on the map
        """
        coef_dict = self.params["room_chances"]
        sum_coefs = sum(coef_dict[key] for key in coef_dict)
        target = randint(1, sum_coefs)
        for key in coef_dict:
            if target > coef_dict[key]:
                target -= coef_dict[key]
            else:
                break

        if key == "circular":
            return self.create_circular_room(spawnable=spawnable)
        elif key == "chunks":
            return self.create_chunk_room(spawnable=spawnable)

    def register_spawn_area(self, area: List[List[Tile]]) -> None:
        """
        Register all floor positions relative to the input grid
        for later use
        """
        spawn_positions = []
        for y, line in enumerate(area):
            for x, tile in enumerate(line):
                if tile == Tile.FLOOR:
                    spawn_positions.append([y, x])
        self.queued_area = spawn_positions

    def update_spawnable(self, y: int, x: int) -> None:
        """
        Convert previous spawn positions relative to the room grid to actual
        actual spawn positions on the level grid, using the position of the
        top left corner of the room on the level, then log them as a
        spawnable region
        """
        if self.queued_area is not None:
            translated_area = [[y + ry, x + rx] for ry, rx in self.queued_area]
            self.spawn_areas.append(translated_area)
        self.queued_area = None

    def populate(self, rv: Map) -> None:
        """
        Populate every spawnable area with some randomly chosen, randomly
        placed entity
        """
        min_c, max_c = self.params["spawn_per_region"]
        for region in self.spawn_areas:
            entity_count = randint(min_c, max_c)
            for _dummy in range(entity_count):
                entity = choices(Entity.get_all_entity_classes(),
                                 weights=Entity.get_weights(), k=1)[0]()
                y, x = choice(region)
                entity.move(y, x)
                rv.add_entity(entity)

    def run(self) -> Map:
        """
        Using procedural generation, build and return a full map, populated
        with entities
        """
        height, width = self.params["height"], self.params["width"]
        level = [width * [Tile.EMPTY] for _ignored in range(height)]

        # the starting room must have no corridor
        mem, self.params["corridor_chance"] = self.params["corridor_chance"], 0
        starting_room, _, _, _, _ = self.create_random_room(spawnable=False)
        dim_v, dim_h = len(starting_room), len(starting_room[0])
        # because Generator.room_fits checks that the exit door is correctly
        # placed, but the starting room has no exit door, we find a positoin
        # manually
        pos_y, pos_x = randint(0, height - dim_v - 1),\
            randint(0, width - dim_h - 1)
        self.place_room(level, pos_y, pos_x, starting_room, 0, 0)
        # remove the door that was placed
        if starting_room[0][0] != Tile.FLOOR:
            level[pos_y][pos_x] = Tile.EMPTY
        self.params["corridor_chance"] = mem

        # find a starting position for the player
        sy, sx = randint(0, height - 1), randint(0, width - 1)
        while level[sy][sx] != Tile.FLOOR:
            sy, sx = randint(0, height - 1), randint(0, width - 1)
        level[sy][sx] = Tile.LADDER

        # now we loop until we're bored, or we've added enough rooms
        tries, rooms_built = 0, 0
        while tries < self.params["tries"] \
                and rooms_built < self.params["max_rooms"]:

            # build a room, try to fit it everywhere in a random order, and
            # place it at the first possible position
            room, door_y, door_x, dy, dx = self.create_random_room()
            positions = [i for i in range(height * width)]
            shuffle(positions)
            for pos in positions:
                y, x = pos // width, pos % width
                if self.room_fits(level, y, x, room, door_y, door_x, dy, dx):
                    self.update_spawnable(y - door_y, x - door_x)
                    self.place_room(level, y, x, room, door_y, door_x)
                    rooms_built += 1
                    break
            tries += 1

        # post-processing
        self.place_walls(level)

        # because when a room is placed, it leads to exactly one previously
        # placed room, the level has a tree like structure with the starting
        # room as the root
        # to avoid boring player backtracking, we add some cycles to the room
        # graph in post processing by placing additional corridors
        tries, loops = 0, 0
        while tries < self.params["loop_tries"] and \
                loops < self.params["loop_max"]:
            tries += 1
            y, x = randint(0, height - 1), randint(0, width - 1)
            loops += self.add_loop(level, y, x)

        # place an exit ladder
        y, x = randint(0, height - 1), randint(0, width - 1)
        while level[y][x] != Tile.FLOOR or \
                any([level[j][i].is_wall() for j, i
                     in Map.neighbourhood(level, y, x, large=True)]):
            y, x = randint(0, height - 1), randint(0, width - 1)
        level[y][x] = Tile.LADDER

        # spawn entities
        rv = Map(width, height, level, sy, sx)
        self.populate(rv)

        return rv
