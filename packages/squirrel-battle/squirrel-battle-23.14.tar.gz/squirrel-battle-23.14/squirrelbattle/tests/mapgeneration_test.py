# Copyright (C) 2020 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

from random import randint
from typing import List
import unittest

from ..display.texturepack import TexturePack
from ..interfaces import Map, Tile
from ..mapgeneration import broguelike


class TestBroguelike(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = broguelike.Generator()
        self.stom = lambda x: Map.load_from_string("0 0\n" + x)
        self.mtos = lambda x: x.draw_string(TexturePack.ASCII_PACK)

    def test_dist(self) -> None:
        m = self.stom(".. ..\n ... ")
        distance = broguelike.dist(m.tiles, 0, 0, 0, 4)
        self.assertEqual(distance, 6)
        m = self.stom(". .")
        distance = broguelike.dist(m.tiles, 0, 0, 0, 2)
        self.assertEqual(distance, -1)

    def is_connex(self, grid: List[List[Tile]]) -> bool:
        h, w = len(grid), len(grid[0])
        y, x = -1, -1
        while not grid[y][x].can_walk():
            y, x = randint(0, h - 1), randint(0, w - 1)
        queue = Map.neighbourhood(grid, y, x)
        while queue:
            y, x = queue.pop()
            if grid[y][x].can_walk() or grid[y][x] == Tile.DOOR:
                grid[y][x] = Tile.WALL
                queue += Map.neighbourhood(grid, y, x)
        return not any([t.can_walk() or t == Tile.DOOR
                        for row in grid for t in row])

    def test_build_doors(self) -> None:
        m = self.stom(".  .\n.  .\n.  .\n")
        self.assertFalse(self.generator.build_door(m.tiles, 1, 1, 0, 1, 2))

    def test_connexity(self) -> None:
        m = self.generator.run()
        self.assertTrue(self.is_connex(m.tiles))

    def test_loops(self) -> None:
        m = self.stom(3 * "..   ..\n")
        self.generator.add_loop(m.tiles, 1, 3)
        s = self.mtos(m)
        self.assertEqual(s, "..   ..\n.......\n..   ..")
        self.assertFalse(self.generator.add_loop(m.tiles, 0, 0))
        m = self.stom("...\n. .\n...")
        self.assertFalse(self.generator.add_loop(m.tiles, 1, 1))
