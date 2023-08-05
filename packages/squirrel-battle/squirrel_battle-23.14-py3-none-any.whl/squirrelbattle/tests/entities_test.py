# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import random
import unittest

from ..entities.friendly import Chest, Trumpet
from ..entities.items import BodySnatchPotion, Bomb, Explosion, Heart, Item
from ..entities.monsters import GiantSeaEagle, Hedgehog, Rabbit, \
    TeddyBear, Tiger
from ..entities.player import Player
from ..interfaces import Entity, Map
from ..resources import ResourceManager


class TestEntities(unittest.TestCase):
    def setUp(self) -> None:
        """
        Loads example map that can be used in tests.
        """
        self.map = Map.load(ResourceManager.get_asset_path("example_map.txt"))
        self.player = Player()
        self.player.constitution = 0
        self.map.add_entity(self.player)
        self.player.move(self.map.start_y, self.map.start_x)

    def test_basic_entities(self) -> None:
        """
        Tests some random stuff with basic entities.
        """
        entity = Entity()
        entity.move(42, 64)
        self.assertEqual(entity.y, 42)
        self.assertEqual(entity.x, 64)
        self.assertIsNone(entity.act(self.map))

        other_entity = Entity()
        other_entity.move(45, 68)
        self.assertEqual(entity.distance_squared(other_entity), 25)
        self.assertEqual(entity.distance(other_entity), 5)

    def test_fighting_entities(self) -> None:
        """
        Tests some random stuff with fighting entities.
        """
        entity = Tiger()
        self.map.add_entity(entity)
        self.assertEqual(entity.maxhealth, 30)
        self.assertEqual(entity.maxhealth, entity.health)
        self.assertEqual(entity.strength, 5)
        for _ in range(5):
            self.assertEqual(entity.hit(entity),
                             "Tiger hits tiger. Tiger takes 5 damage.")
            self.assertFalse(entity.dead)
        self.assertEqual(entity.hit(entity), "Tiger hits tiger. "
                         + "Tiger takes 5 damage. Tiger dies.")
        self.assertTrue(entity.dead)

        entity = Rabbit()
        entity.health = 15
        entity.critical = 0
        self.map.add_entity(entity)
        entity.move(15, 44)
        # Move randomly
        self.map.tick(self.player)
        self.assertFalse(entity.y == 15 and entity.x == 44)

        # Move to the player
        entity.move(3, 6)
        self.map.tick(self.player)
        self.assertTrue(entity.y == 2 and entity.x == 6)

        # Rabbit should fight
        old_health = self.player.health
        self.map.tick(self.player)
        self.assertTrue(entity.y == 2 and entity.x == 6)
        self.assertEqual(old_health - entity.strength, self.player.health)
        self.assertEqual(self.map.logs.messages[-1],
                         f"{entity.name.capitalize()} hits {self.player.name}. \
{self.player.name.capitalize()} takes {entity.strength} damage.")

        # Fight the rabbit
        self.player.critical = 0
        old_health = entity.health
        self.player.move_down()
        self.assertEqual(entity.health, old_health - self.player.strength)
        self.assertFalse(entity.dead)
        old_health = entity.health
        self.player.move_down()
        self.assertEqual(entity.health, old_health - self.player.strength)
        self.assertFalse(entity.dead)
        old_health = entity.health
        self.player.move_down()
        self.assertEqual(entity.health, old_health - self.player.strength)
        self.assertTrue(entity.dead)
        self.assertGreaterEqual(self.player.current_xp, 3)

        # Test that a chest is destroyed by a bomb
        bomb = Bomb()
        bomb.owner = self.player
        bomb.move(3, 6)
        self.map.add_entity(bomb)
        chest = Chest()
        chest.move(4, 6)
        self.map.add_entity(chest)
        bomb.exploding = True
        for _ in range(5):
            self.map.tick(self.player)
        self.assertTrue(chest.annihilated)

    def test_familiar(self) -> None:
        fam = Trumpet()
        entity = Rabbit()
        self.map.add_entity(entity)
        self.map.add_entity(fam)
        self.player.move(1, 6)
        entity.move(2, 6)
        fam.move(2, 7)

        # Test fighting
        entity.health = 2
        entity.paths = []
        entity.recalculate_paths()
        fam.target = entity
        self.map.tick(self.player)
        self.assertTrue(entity.dead)

        # Test finding a new target
        entity2 = Rabbit()
        self.map.add_entity(entity2)
        entity2.move(2, 6)
        self.map.tick(self.player)
        self.assertTrue(fam.target == entity2)
        self.map.remove_entity(entity2)

        # Test following the player and finding the player as target
        self.player.move(6, 5)
        fam.move(5, 5)
        fam.target = None
        self.player.move_down()
        self.map.tick(self.player)
        self.assertTrue(fam.target == self.player)
        self.assertEqual(fam.y, 6)
        self.assertEqual(fam.x, 5)

        # Test random move
        fam.move(13, 20)
        fam.target = self.player
        self.map.tick(self.player)
        self.assertTrue(fam.x != 20 or fam.y != 13)

    def test_items(self) -> None:
        """
        Tests some random stuff with items.
        """
        item = Item()
        self.map.add_entity(item)
        self.assertIsNone(item.held_by)
        item.hold(self.player)
        self.assertEqual(item.held_by, self.player)
        item.drop()
        self.assertEqual(item.y, 1)
        self.assertEqual(item.x, 6)

        # Pick up item
        self.player.move_left()
        self.player.move_right()
        self.assertEqual(item.held_by, self.player)
        self.assertIn(item, self.player.inventory)
        self.assertNotIn(item, self.map.entities)

    def test_bombs(self) -> None:
        """
        Tests some random stuff with bombs.
        """
        item = Bomb()
        hedgehog = Hedgehog()
        teddy_bear = TeddyBear()
        self.map.add_entity(item)
        self.map.add_entity(hedgehog)
        self.map.add_entity(teddy_bear)
        hedgehog.health = 2
        teddy_bear.health = 2
        hedgehog.move(41, 42)
        teddy_bear.move(42, 41)
        item.act(self.map)
        self.assertFalse(hedgehog.dead)
        self.assertFalse(teddy_bear.dead)
        self.player.move(42, 42)
        item.hold(self.player)
        item.use()
        self.assertEqual(item.y, 42)
        self.assertEqual(item.x, 42)
        # Wait for the explosion
        for _ignored in range(5):
            item.act(self.map)
        self.assertTrue(hedgehog.dead)
        self.assertTrue(teddy_bear.dead)
        bomb_state = item.save_state()
        self.assertEqual(bomb_state["damage"], item.damage)
        explosions = self.map.find_entities(Explosion)
        self.assertTrue(explosions)
        explosion = explosions[0]
        self.assertEqual(explosion.y, item.y)
        self.assertEqual(explosion.x, item.x)

        # The player can't hold the explosion
        explosion.hold(self.player)
        self.assertNotIn(explosion, self.player.inventory)
        self.assertIsNone(explosion.held_by)

        # The explosion disappears after one tick
        explosion.act(self.map)
        self.assertNotIn(explosion, self.map.entities)

    def test_hearts(self) -> None:
        """
        Tests some random stuff with hearts.
        """
        item = Heart()
        self.map.add_entity(item)
        item.move(2, 6)
        self.player.health -= 2 * item.healing
        self.player.move_down()
        self.assertNotIn(item, self.map.entities)
        self.assertEqual(self.player.health,
                         self.player.maxhealth - item.healing)
        heart_state = item.save_state()
        self.assertEqual(heart_state["healing"], item.healing)

    def test_body_snatch_potion(self) -> None:
        """
        Tests some random stuff with body snatch potions.
        """
        item = BodySnatchPotion()
        self.map.add_entity(item)
        item.hold(self.player)

        tiger = Tiger(y=42, x=42)
        self.map.add_entity(tiger)

        # The player becomes a tiger, and the tiger becomes a squirrel
        item.use()
        self.assertEqual(self.player.name, "tiger")
        self.assertEqual(tiger.name, "player")
        self.assertEqual(self.player.y, 42)
        self.assertEqual(self.player.x, 42)

    def test_players(self) -> None:
        """
        Tests some random stuff with players.
        """
        player = Player()
        self.map.add_entity(player)
        player.move(1, 6)
        self.assertEqual(player.strength, 5)
        self.assertEqual(player.health, player.maxhealth)
        self.assertEqual(player.maxhealth, 20)

        # Test movements and ensure that collisions are working
        self.assertFalse(player.move_up())
        self.assertTrue(player.move_left())
        self.assertFalse(player.move_left())
        for _ in range(8):
            self.assertTrue(player.move_down())
        self.assertFalse(player.move_down())
        self.assertTrue(player.move_right())
        self.assertTrue(player.move_right())
        self.assertTrue(player.move_right())
        self.assertFalse(player.move_right())
        self.assertTrue(player.move_down())
        self.assertTrue(player.move_down())

        player.add_xp(70)
        self.assertEqual(player.current_xp, 10)
        self.assertEqual(player.max_xp, 40)
        self.assertEqual(player.level, 4)

        player_state = player.save_state()
        self.assertEqual(player_state["current_xp"], 10)

        player = Player()
        player.map = self.map
        player.add_xp(700)
        for _ in range(13):
            player.level_up()
        self.assertEqual(player.level, 12)
        self.assertEqual(player.critical, 5 + 95 // 30)
        self.assertEqual(player.charisma, 3)

    def test_critical_hit(self) -> None:
        """
        Ensure that critical hits are working.
        """
        random.seed(2)  # Next random.randint(1, 100) will output 8
        self.player.critical = 10
        sea_eagle = GiantSeaEagle()
        self.map.add_entity(sea_eagle)
        sea_eagle.move(2, 6)
        old_health = sea_eagle.health
        self.player.hit(sea_eagle)
        self.assertEqual(sea_eagle.health,
                         old_health - self.player.strength * 4)
