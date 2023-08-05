# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from ..display.texturepack import TexturePack
from ..interfaces import Map, Slope, Tile
from ..resources import ResourceManager


class TestInterfaces(unittest.TestCase):
    def test_map(self) -> None:
        """
        Creates a map and checks that it is well parsed.
        """
        m = Map.load_from_string("0 0\n.#\n#.\n")
        self.assertEqual(m.width, 2)
        self.assertEqual(m.height, 2)
        self.assertEqual(m.draw_string(TexturePack.ASCII_PACK), ".#\n#.")

    def test_load_map(self) -> None:
        """
        Tries to load a map from a file.
        """
        m = Map.load(ResourceManager.get_asset_path("example_map.txt"))
        self.assertEqual(m.width, 52)
        self.assertEqual(m.height, 17)

    def test_tiles(self) -> None:
        """
        Tests some things about tiles.
        """
        self.assertFalse(Tile.FLOOR.is_wall())
        self.assertTrue(Tile.WALL.is_wall())
        self.assertFalse(Tile.EMPTY.is_wall())
        self.assertTrue(Tile.FLOOR.can_walk())
        self.assertFalse(Tile.WALL.can_walk())
        self.assertFalse(Tile.EMPTY.can_walk())
        self.assertRaises(ValueError, Tile.from_ascii_char, 'unknown')

    def test_slope(self) -> None:
        """
        Test good behaviour of slopes (basically vectors, compared according to
        the determinant)
        """
        a = Slope(1, 1)
        b = Slope(0, 1)
        self.assertTrue(b < a)
        self.assertTrue(b <= a)
        self.assertTrue(a <= a)
        self.assertTrue(a == a)
        self.assertTrue(a > b)
        self.assertTrue(a >= b)

    # def test_visibility(self) -> None:
        # m = Map.load(ResourceManager.get_asset_path("example_map_3.txt"))
        # m.compute_visibility(1, 1, 50)
