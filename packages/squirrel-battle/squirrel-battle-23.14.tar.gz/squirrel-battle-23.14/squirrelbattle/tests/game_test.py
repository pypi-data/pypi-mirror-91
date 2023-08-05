# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import curses
import unittest

from ..bootstrap import Bootstrap
from ..display.display import Display
from ..display.display_manager import DisplayManager
from ..entities.friendly import Chest, Merchant, Sunflower
from ..entities.items import Bomb, Bow, Chestplate, Explosion, FireBallStaff, \
    Heart, Helmet, Monocle, RingCritical, ScrollofDamage, ScrollofWeakening, \
    Shield, Sword
from ..entities.monsters import GiantSeaEagle, Rabbit
from ..entities.player import Player
from ..enums import DisplayActions, GameMode, KeyValues
from ..game import Game
from ..interfaces import Map, Tile
from ..menus import MainMenuValues
from ..resources import ResourceManager
from ..settings import Settings
from ..translations import gettext as _, Translator


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        """
        Sets the game up.
        """
        self.game = Game()
        self.game.new_game()
        self.game.map = Map.load(
            ResourceManager.get_asset_path("example_map.txt"))
        self.game.map.add_entity(self.game.player)
        self.game.player.move(self.game.map.start_y, self.game.map.start_x)
        self.game.logs.add_message("Hello World !")
        display = DisplayManager(None, self.game)
        self.game.display_actions = display.handle_display_action

    def test_load_game(self) -> None:
        """
        Saves a game and reloads it.
        """
        bomb = Bomb()
        self.game.map.add_entity(bomb)
        sword = Sword()
        self.game.map.add_entity(sword)
        # Add items in the inventory to check that it is well loaded
        bomb.hold(self.game.player)
        sword.hold(self.game.player)
        sword.equip()

        # Ensure that merchants can be saved
        merchant = Merchant()
        merchant.move(3, 6)
        self.game.map.add_entity(merchant)

        old_state = self.game.save_state()

        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(), MainMenuValues.SAVE)
        self.game.handle_key_pressed(KeyValues.ENTER)  # Save game
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(), MainMenuValues.LOAD)
        self.game.handle_key_pressed(KeyValues.ENTER)  # Load game

        new_state = self.game.save_state()
        self.assertEqual(old_state, new_state)
        self.assertIsNone(self.game.message)

        # Ensure that the bomb is loaded
        self.assertTrue(self.game.player.inventory)

        # Error on loading save
        with open(ResourceManager.get_config_path("save.json"), "w") as f:
            f.write("I am not a JSON file")
        self.assertIsNone(self.game.message)
        self.game.load_game()
        self.assertIsNotNone(self.game.message)
        self.game.message = None

        with open(ResourceManager.get_config_path("save.json"), "w") as f:
            f.write("{}")
        self.assertIsNone(self.game.message)
        self.game.load_game()
        self.assertIsNotNone(self.game.message)
        self.game.message = None

        # Load game with a dead player
        self.game.map.remove_entity(self.game.player)
        self.game.save_game()
        self.game.load_game()
        self.assertIsNotNone(self.game.message)

    def test_bootstrap_fail(self) -> None:
        """
        Ensures that the test can't play the game,
        because there is no associated shell.
        Yeah, that's only for coverage.
        """
        self.assertRaises(Exception, Bootstrap.run_game)

    def test_key_translation(self) -> None:
        """
        Tests key bindings.
        """
        self.game.settings = Settings()

        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_UP_PRIMARY, self.game.settings),
            KeyValues.UP)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_UP_SECONDARY, self.game.settings),
            KeyValues.UP)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_DOWN_PRIMARY, self.game.settings),
            KeyValues.DOWN)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_DOWN_SECONDARY, self.game.settings),
            KeyValues.DOWN)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_LEFT_PRIMARY, self.game.settings),
            KeyValues.LEFT)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_LEFT_SECONDARY, self.game.settings),
            KeyValues.LEFT)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_RIGHT_PRIMARY, self.game.settings),
            KeyValues.RIGHT)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_RIGHT_SECONDARY, self.game.settings),
            KeyValues.RIGHT)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_ENTER, self.game.settings),
            KeyValues.ENTER)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_INVENTORY, self.game.settings),
            KeyValues.INVENTORY)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_CHAT, self.game.settings),
            KeyValues.CHAT)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_USE, self.game.settings),
            KeyValues.USE)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_EQUIP, self.game.settings),
            KeyValues.EQUIP)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_DROP, self.game.settings),
            KeyValues.DROP)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_WAIT, self.game.settings),
            KeyValues.WAIT)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_LADDER, self.game.settings),
            KeyValues.LADDER)
        self.assertEqual(KeyValues.translate_key(' ', self.game.settings),
                         KeyValues.SPACE)
        self.assertEqual(KeyValues.translate_key('plop', self.game.settings),
                         None)
        self.assertEqual(KeyValues.translate_key(
            self.game.settings.KEY_DANCE, self.game.settings),
            KeyValues.DANCE)

    def test_key_press(self) -> None:
        """
        Presses a key and asserts what is done is correct.
        """
        self.assertEqual(self.game.state, GameMode.MAINMENU)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.START)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.START)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.RESUME)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.SAVE)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.LOAD)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.SETTINGS)
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.state, GameMode.SETTINGS)

        self.game.handle_key_pressed(KeyValues.SPACE)
        self.assertEqual(self.game.state, GameMode.MAINMENU)

        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.EXIT)
        self.assertRaises(SystemExit, self.game.handle_key_pressed,
                          KeyValues.ENTER)

        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.SETTINGS)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.LOAD)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.SAVE)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.RESUME)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.main_menu.validate(),
                         MainMenuValues.START)

        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.state, GameMode.PLAY)

        # Kill entities
        for entity in self.game.map.entities.copy():
            if not isinstance(entity, Player):
                self.game.map.remove_entity(entity)

        y, x = self.game.player.y, self.game.player.x

        # Ensure that the neighborhood is walkable
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                self.game.map.tiles[y + dy][x + dx] = Tile.FLOOR

        self.game.handle_key_pressed(KeyValues.DOWN)
        new_y, new_x = self.game.player.y, self.game.player.x
        self.assertEqual(new_y, y + 1)
        self.assertEqual(new_x, x)

        y, x = new_y, new_x
        self.game.handle_key_pressed(KeyValues.RIGHT)
        new_y, new_x = self.game.player.y, self.game.player.x
        self.assertEqual(new_y, y)
        self.assertEqual(new_x, x + 1)

        y, x = self.game.player.y, self.game.player.x
        self.game.handle_key_pressed(KeyValues.UP)
        new_y, new_x = self.game.player.y, self.game.player.x
        self.assertEqual(new_y, y - 1)
        self.assertEqual(new_x, x)

        y, x = self.game.player.y, self.game.player.x
        self.game.handle_key_pressed(KeyValues.LEFT)
        new_y, new_x = self.game.player.y, self.game.player.x
        self.assertEqual(new_y, y)
        self.assertEqual(new_x, x - 1)

        explosion = Explosion()
        self.game.map.add_entity(explosion)
        self.assertIn(explosion, self.game.map.entities)
        self.game.handle_key_pressed(KeyValues.WAIT)
        self.assertNotIn(explosion, self.game.map.entities)

        rabbit = Rabbit()
        self.game.map.add_entity(rabbit)
        self.game.player.move(1, 6)
        rabbit.move(3, 6)
        self.game.player.charisma = 11
        self.game.handle_key_pressed(KeyValues.DANCE)
        self.assertEqual(rabbit.confused, 1)
        string = rabbit.hit(self.game.player)
        self.assertEqual(
            string, _("{name} is confused, it can not hit {opponent}.")
            .format(name=rabbit.translated_name.capitalize(),
                    opponent=self.game.player.translated_name))
        rabbit.confused = 0
        self.game.player.charisma = 0
        self.game.handle_key_pressed(KeyValues.DANCE)
        self.assertEqual(rabbit.confused, 0)
        rabbit.die()

        self.game.player.charisma = 11
        self.game.handle_key_pressed(KeyValues.DANCE)
        self.game.player.charisma = 1

        self.game.handle_key_pressed(KeyValues.SPACE)
        self.assertEqual(self.game.state, GameMode.MAINMENU)

    def test_mouse_click(self) -> None:
        """
        Simulates mouse clicks.
        """
        self.game.state = GameMode.MAINMENU

        # Change the color of the artwork
        self.game.display_actions(DisplayActions.MOUSE, 0, 10,
                                  curses.BUTTON1_CLICKED)

        # Settings menu
        self.game.display_actions(DisplayActions.MOUSE, 25, 21,
                                  curses.BUTTON1_CLICKED)
        self.assertEqual(self.game.main_menu.position, 4)
        self.assertEqual(self.game.state, GameMode.SETTINGS)

        bomb = Bomb()
        bomb.hold(self.game.player)
        bomb2 = Bomb()
        bomb2.hold(self.game.player)

        self.game.state = GameMode.INVENTORY

        # Click nowhere
        self.game.display_actions(DisplayActions.MOUSE, 0, 0,
                                  curses.BUTTON1_CLICKED)
        self.assertEqual(self.game.state, GameMode.INVENTORY)

        # Click on the second item
        self.game.display_actions(DisplayActions.MOUSE, 8, 25,
                                  curses.BUTTON1_CLICKED)
        self.assertEqual(self.game.state, GameMode.INVENTORY)
        self.assertEqual(self.game.inventory_menu.position, 1)

    def test_new_game(self) -> None:
        """
        Ensures that the start button starts a new game.
        """
        old_map = self.game.map
        old_player = self.game.player
        self.game.handle_key_pressed(KeyValues.ENTER)  # Start new game
        new_map = self.game.map
        new_player = self.game.player
        # Ensure that
        self.assertNotEqual(old_map, new_map)
        self.assertNotEqual(old_player, new_player)

        self.game.handle_key_pressed(KeyValues.SPACE)
        old_map = new_map
        old_player = new_player
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.ENTER)  # Resume game
        new_map = self.game.map
        new_player = self.game.player
        self.assertEqual(old_map, new_map)
        self.assertEqual(old_player, new_player)

    def test_settings_menu(self) -> None:
        """
        Ensures that the settings menu is working properly.
        """
        self.game.settings = Settings()

        # Open settings menu
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.state, GameMode.SETTINGS)

        # Define the "move up" key to 'h'
        self.assertFalse(self.game.settings_menu.waiting_for_key)
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertTrue(self.game.settings_menu.waiting_for_key)
        self.game.handle_key_pressed(None, 'h')
        self.assertFalse(self.game.settings_menu.waiting_for_key)
        self.assertEqual(self.game.settings.KEY_UP_PRIMARY, 'h')

        # Navigate to "move left"
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.UP)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)

        # Define the "move up" key to 'a'
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertTrue(self.game.settings_menu.waiting_for_key)
        # Can't used a mapped key
        self.game.handle_key_pressed(None, 's')
        self.assertTrue(self.game.settings_menu.waiting_for_key)
        self.game.handle_key_pressed(None, 'a')
        self.assertFalse(self.game.settings_menu.waiting_for_key)
        self.assertEqual(self.game.settings.KEY_LEFT_PRIMARY, 'a')

        # Navigate to "texture pack"
        for ignored in range(14):
            self.game.handle_key_pressed(KeyValues.DOWN)

        # Change texture pack
        self.assertEqual(self.game.settings.TEXTURE_PACK, "ascii")
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.settings.TEXTURE_PACK, "squirrel")
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.settings.TEXTURE_PACK, "ascii")

        # Change language
        Translator.compilemessages()
        Translator.refresh_translations()
        self.game.settings.LOCALE = "en"
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.settings.LOCALE, "fr")
        self.assertEqual(_("New game"), "Nouvelle partie")
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.settings.LOCALE, "de")
        self.assertEqual(_("New game"), "Neu Spiel")
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.settings.LOCALE, "es")
        self.assertEqual(_("New game"), "Nuevo partido")
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.settings.LOCALE, "en")
        self.assertEqual(_("New game"), "New game")

        # Navigate to "back" button
        self.game.handle_key_pressed(KeyValues.DOWN)

        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertEqual(self.game.state, GameMode.MAINMENU)

    def test_logs(self) -> None:
        """
        Tests the use of logs
        """
        self.assertEqual(self.game.logs.messages, ["Hello World !"])
        self.game.logs.add_messages(["Hello", "World"])
        self.assertEqual(self.game.logs.messages, ["Hello World !",
                                                   "Hello", "World"])
        self.game.logs.clear()
        self.assertEqual(self.game.logs.messages, [])

    def test_dead_screen(self) -> None:
        """
        Kills the player and renders the dead message on the fake screen.
        """
        self.game.state = GameMode.PLAY
        # Kill player
        self.game.player.take_damage(self.game.player,
                                     self.game.player.health + 2)
        y, x = self.game.player.y, self.game.player.x
        for key in [KeyValues.UP, KeyValues.DOWN,
                    KeyValues.LEFT, KeyValues.RIGHT]:
            self.game.handle_key_pressed(key)
            new_y, new_x = self.game.player.y, self.game.player.x
            self.assertEqual(new_y, y)
            self.assertEqual(new_x, x)

    def test_not_implemented(self) -> None:
        """
        Checks that some functions are not implemented, only for coverage.
        """
        self.assertRaises(NotImplementedError, Display.display, None)
        self.assertRaises(NotImplementedError, Display.update, None, self.game)

    def test_messages(self) -> None:
        """
        Displays error messages.
        """
        self.game.message = "I am an error"
        self.game.display_actions(DisplayActions.UPDATE)
        self.game.display_actions(DisplayActions.REFRESH)
        self.game.handle_key_pressed(None, "random key")
        self.assertIsNone(self.game.message)

    def test_inventory_menu(self) -> None:
        """
        Opens the inventory menu and interacts with items.
        """
        self.game.state = GameMode.PLAY
        # Open and close the inventory
        self.game.handle_key_pressed(KeyValues.INVENTORY)
        self.assertEqual(self.game.state, GameMode.INVENTORY)
        self.game.handle_key_pressed(KeyValues.SPACE)
        self.assertEqual(self.game.state, GameMode.PLAY)

        # Add five bombs in the inventory
        for ignored in range(5):
            bomb = Bomb()
            bomb.map = self.game.map
            bomb.map.add_entity(bomb)
            bomb.hold(self.game.player)

        self.game.handle_key_pressed(KeyValues.INVENTORY)
        self.assertEqual(self.game.state, GameMode.INVENTORY)

        # Navigate in the menu
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.inventory_menu.position, 3)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.UP)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.inventory_menu.position, 4)

        # Equip key does nothing
        self.game.handle_key_pressed(KeyValues.EQUIP)

        # Drop an item
        bomb = self.game.player.inventory[-1]
        self.assertEqual(self.game.inventory_menu.validate(), bomb)
        self.assertEqual(bomb.held_by, self.game.player)
        self.game.handle_key_pressed(KeyValues.DROP)
        self.assertIsNone(bomb.held_by)
        self.assertIsNone(bomb.owner)
        self.assertFalse(bomb.exploding)
        self.assertEqual(bomb.y, self.game.player.y)
        self.assertEqual(bomb.x, self.game.player.x)

        # Use the bomb
        bomb = self.game.player.inventory[-1]
        self.assertEqual(self.game.inventory_menu.validate(), bomb)
        self.assertEqual(bomb.held_by, self.game.player)
        self.game.handle_key_pressed(KeyValues.USE)
        self.assertIsNone(bomb.held_by)
        self.assertEqual(bomb.owner, self.game.player)
        self.assertTrue(bomb.exploding)
        self.assertEqual(bomb.y, self.game.player.y)
        self.assertEqual(bomb.x, self.game.player.x)

    def test_talk_to_sunflowers(self) -> None:
        """
        Interacts with sunflowers.
        """
        self.game.state = GameMode.PLAY

        sunflower = Sunflower()
        sunflower.move(self.game.player.y + 1, self.game.player.x)
        self.game.map.add_entity(sunflower)

        # Does nothing
        self.assertIsNone(self.game.handle_friendly_entity_chat(KeyValues.UP))

        # Talk to sunflower... or not
        self.game.handle_key_pressed(KeyValues.CHAT)
        self.assertTrue(self.game.waiting_for_friendly_key)
        # Wrong key
        self.game.handle_key_pressed(KeyValues.EQUIP)
        self.assertFalse(self.game.waiting_for_friendly_key)
        self.game.handle_key_pressed(KeyValues.CHAT)
        self.assertTrue(self.game.waiting_for_friendly_key)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertFalse(self.game.waiting_for_friendly_key)
        self.assertEqual(self.game.state, GameMode.PLAY)
        self.assertFalse(len(self.game.logs.messages) > 1)

        # Talk to sunflower
        self.game.handle_key_pressed(KeyValues.CHAT)
        self.assertTrue(self.game.waiting_for_friendly_key)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertFalse(self.game.waiting_for_friendly_key)
        self.assertEqual(self.game.state, GameMode.PLAY)
        self.assertTrue(self.game.logs.messages)
        # Ensure that the message is a good message
        self.assertTrue(any(self.game.logs.messages[1].endswith(msg)
                            for msg in Sunflower().dialogue_option))

        # Test all directions to detect the friendly entity
        self.game.player.move(sunflower.y + 1, sunflower.x)
        self.game.handle_key_pressed(KeyValues.CHAT)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(len(self.game.logs.messages), 3)
        self.game.player.move(sunflower.y, sunflower.x + 1)
        self.game.handle_key_pressed(KeyValues.CHAT)
        self.game.handle_key_pressed(KeyValues.LEFT)
        self.assertEqual(len(self.game.logs.messages), 4)
        self.game.player.move(sunflower.y, sunflower.x - 1)
        self.game.handle_key_pressed(KeyValues.CHAT)
        self.game.handle_key_pressed(KeyValues.RIGHT)
        self.assertEqual(len(self.game.logs.messages), 5)

    def test_talk_to_merchant(self) -> None:
        """
        Interacts with merchants.
        """
        self.game.state = GameMode.PLAY

        merchant = Merchant()
        merchant.move(self.game.player.y + 1, self.game.player.x)
        self.game.map.add_entity(merchant)

        # Does nothing
        self.assertIsNone(self.game.handle_friendly_entity_chat(KeyValues.UP))

        # Talk to merchant
        self.game.handle_key_pressed(KeyValues.CHAT)
        self.assertTrue(self.game.waiting_for_friendly_key)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertFalse(self.game.waiting_for_friendly_key)
        self.assertEqual(self.game.state, GameMode.STORE)
        self.assertTrue(self.game.logs.messages)

        # Navigate in the menu
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.LEFT)
        self.assertFalse(self.game.is_in_store_menu)
        self.game.handle_key_pressed(KeyValues.RIGHT)
        self.assertTrue(self.game.is_in_store_menu)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.store_menu.position, 1)

        self.game.player.hazel = 0x7ffff42ff

        # The second item is not a heart
        merchant.inventory[1] = sword = Sword()
        # Buy the second item by clicking on it
        item = self.game.store_menu.validate()
        self.assertIn(item, merchant.inventory)
        self.game.display_actions(DisplayActions.MOUSE, 7, 25,
                                  curses.BUTTON1_CLICKED)
        self.assertIn(item, self.game.player.inventory)
        self.assertNotIn(item, merchant.inventory)

        # Buy a heart
        merchant.inventory[1] = Heart()
        self.game.display_actions(DisplayActions.REFRESH)
        item = self.game.store_menu.validate()
        self.assertIn(item, merchant.inventory)
        self.assertEqual(item, merchant.inventory[1])
        self.game.player.health = self.game.player.maxhealth - 1 - item.healing
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertNotIn(item, self.game.player.inventory)
        self.assertNotIn(item, merchant.inventory)
        self.assertEqual(self.game.player.health,
                         self.game.player.maxhealth - 1)

        # We don't have enough of money
        self.game.player.hazel = 0
        item = self.game.store_menu.validate()
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertNotIn(item, self.game.player.inventory)
        self.assertIn(item, merchant.inventory)
        self.assertEqual(self.game.message,
                         _("The buyer does not have enough money"))
        self.game.handle_key_pressed(KeyValues.ENTER)

        # Sell an item
        self.game.inventory_menu.position = len(self.game.player.inventory) - 1
        self.game.handle_key_pressed(KeyValues.LEFT)
        self.assertFalse(self.game.is_in_store_menu)
        self.assertIn(sword, self.game.player.inventory)
        self.assertEqual(self.game.inventory_menu.validate(), sword)
        old_player_money, old_merchant_money = self.game.player.hazel,\
            merchant.hazel
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertNotIn(sword, self.game.player.inventory)
        self.assertIn(sword, merchant.inventory)
        self.assertEqual(self.game.player.hazel, old_player_money + sword.price)
        self.assertEqual(merchant.hazel, old_merchant_money - sword.price)

        # Exit the menu
        self.game.handle_key_pressed(KeyValues.SPACE)
        self.assertEqual(self.game.state, GameMode.PLAY)

    def test_equipment(self) -> None:
        """
        Ensure that equipment is working.
        """
        self.game.state = GameMode.INVENTORY

        # sword goes into the main equipment slot
        sword = Sword()
        sword.hold(self.game.player)
        self.game.handle_key_pressed(KeyValues.EQUIP)
        self.assertEqual(self.game.player.equipped_main, sword)

        # shield goes into the secondary equipment slot
        shield = Shield()
        shield.hold(self.game.player)
        shield.equip()
        self.assertEqual(self.game.player.equipped_secondary, shield)

        # helmet goes into the helmet slot
        helmet = Helmet()
        helmet.hold(self.game.player)
        helmet.equip()
        self.assertEqual(self.game.player.equipped_helmet, helmet)

        # helmet goes into the armor slot
        chestplate = Chestplate()
        chestplate.hold(self.game.player)
        chestplate.equip()
        self.assertEqual(self.game.player.equipped_armor, chestplate)

        # Use bomb
        bomb = Bomb()
        bomb.hold(self.game.player)
        bomb.equip()
        self.assertEqual(self.game.player.equipped_secondary, bomb)
        self.assertFalse(shield.equipped)
        self.game.state = GameMode.PLAY
        self.game.handle_key_pressed(KeyValues.USE)
        self.assertIsNone(self.game.player.equipped_secondary)
        self.game.state = GameMode.INVENTORY
        shield.equip()
        self.assertEqual(self.game.player.equipped_secondary, shield)

        # Reequip, which is useless but covers code
        sword.equip()
        shield.equip()
        helmet.equip()
        chestplate.equip()
        self.game.save_state()

        # Unequip all
        sword.unequip()
        shield.unequip()
        helmet.unequip()
        chestplate.unequip()
        self.assertIsNone(self.game.player.equipped_main)
        self.assertIsNone(self.game.player.equipped_secondary)
        self.assertIsNone(self.game.player.equipped_helmet)
        self.assertIsNone(self.game.player.equipped_armor)
        self.assertIn(sword, self.game.player.inventory)
        self.assertIn(shield, self.game.player.inventory)
        self.assertIn(helmet, self.game.player.inventory)
        self.assertIn(chestplate, self.game.player.inventory)
        self.game.display_actions(DisplayActions.REFRESH)

        # Test rings
        self.game.player.inventory.clear()
        ring = RingCritical()
        ring.hold(self.game.player)
        self.game.display_actions(DisplayActions.REFRESH)
        old_critical = self.game.player.critical
        self.game.handle_key_pressed(KeyValues.EQUIP)
        self.assertEqual(self.game.player.critical,
                         old_critical + ring.critical)
        self.game.save_state()
        ring.unequip()

    def test_monocle(self) -> None:
        """
        The player is wearing a monocle, then the stats are displayed.
        """
        self.game.state = GameMode.PLAY

        monocle = Monocle()
        monocle.hold(self.game.player)
        monocle.equip()

        sea_eagle = GiantSeaEagle()
        self.game.map.add_entity(sea_eagle)
        sea_eagle.move(2, 6)

        self.game.display_actions(DisplayActions.REFRESH)

    def test_ladders(self) -> None:
        """
        Ensure that the player can climb on ladders.
        """
        self.game.state = GameMode.PLAY

        self.assertEqual(self.game.player.map.floor, 0)
        self.game.handle_key_pressed(KeyValues.LADDER)
        self.assertEqual(self.game.player.map.floor, 0)

        # Move nowhere
        self.game.player.move(10, 10)
        self.game.handle_key_pressed(KeyValues.LADDER)
        self.assertEqual(self.game.player.map.floor, 0)

        # Move down
        self.game.player.move(3, 40)  # Move on a ladder
        self.game.handle_key_pressed(KeyValues.LADDER)
        self.assertEqual(self.game.map_index, 1)
        self.assertEqual(self.game.player.map.floor, 1)
        self.game.display_actions(DisplayActions.UPDATE)

        # Move up
        self.game.handle_key_pressed(KeyValues.LADDER)
        self.assertEqual(self.game.player.map.floor, 0)
        self.assertEqual(self.game.player.y, 3)
        self.assertEqual(self.game.player.x, 40)
        self.game.display_actions(DisplayActions.UPDATE)

    def test_credits(self) -> None:
        """
        Load credits menu.
        """
        self.game.state = GameMode.MAINMENU

        self.game.display_actions(DisplayActions.MOUSE, 41, 41,
                                  curses.BUTTON1_CLICKED)
        self.assertEqual(self.game.state, GameMode.CREDITS)
        self.game.display_actions(DisplayActions.MOUSE, 21, 21,
                                  curses.BUTTON1_CLICKED)
        self.game.display_actions(DisplayActions.REFRESH)

        self.game.state = GameMode.CREDITS
        self.game.handle_key_pressed(KeyValues.ENTER)

        self.assertEqual(self.game.state, GameMode.MAINMENU)

    def test_launch(self) -> None:
        """
        Use the long range weapons to kill some entities.
        """
        self.game.state = GameMode.PLAY
        self.game.player.move(2, 6)

        b = Bow()
        b.held_by = self.game.player
        self.game.player.equipped_main = b
        self.assertTrue(self.game.player.equipped_main)

        entity = Rabbit()
        entity.health = 1
        self.game.map.add_entity(entity)
        entity.move(3, 6)

        self.game.handle_launch(KeyValues.UP)

        self.game.waiting_for_launch_key = True
        self.game.handle_key_pressed(KeyValues.CHAT)

        entity = Rabbit()
        entity.health = 1
        self.game.map.add_entity(entity)
        entity.move(2, 8)
        self.game.waiting_for_launch_key = True
        self.game.handle_key_pressed(KeyValues.RIGHT)

        entity = Rabbit()
        entity.health = 1
        self.game.map.add_entity(entity)
        entity.move(2, 5)
        self.game.waiting_for_launch_key = True
        self.game.handle_key_pressed(KeyValues.LEFT)

        key = "l"
        KeyValues.translate_key(key, self.game.settings)

        self.game.handle_key_pressed(KeyValues.LAUNCH)
        self.assertTrue(self.game.waiting_for_launch_key)
        self.game.handle_key_pressed(KeyValues.DOWN)

        self.assertTrue(entity.dead)

        entity2 = Rabbit()
        entity2.health = 1
        self.game.map.add_entity(entity2)
        entity2.move(1, 6)

        b = FireBallStaff()
        self.game.player.inventory.append(b)
        b.held_by = self.game.player
        b.equip()

        self.game.handle_key_pressed(KeyValues.LAUNCH)
        self.assertTrue(self.game.waiting_for_launch_key)
        self.game.handle_key_pressed(KeyValues.UP)

        self.assertTrue(entity2.dead)

    def test_scrolls(self) -> None:
        """
        Use the scrolls.
        """
        self.game.state = GameMode.PLAY
        self.game.player.move(2, 6)

        entity = Rabbit()
        self.game.map.add_entity(entity)
        entity.move(3, 6)

        entity2 = GiantSeaEagle()
        self.game.map.add_entity(entity2)
        entity2.move(3, 8)

        scroll1 = ScrollofDamage()
        scroll2 = ScrollofWeakening()
        self.game.player.inventory.append(scroll1)
        self.game.player.inventory.append(scroll2)
        scroll1.held_by = self.game.player
        scroll2.held_by = self.game.player

        scroll1.use()
        self.assertTrue(entity.health != entity.maxhealth)
        self.assertTrue(entity2.health != entity2.maxhealth)

        scroll2.use()
        self.assertEqual(entity.strength, 0)
        self.assertEqual(entity2.strength, 999)

        self.game.map.tick(self.game.player)
        self.game.map.tick(self.game.player)
        self.game.map.tick(self.game.player)

        self.assertEqual(entity2.effects, [])

    def test_chests(self) -> None:
        """
        Interacts with chests.
        """
        self.game.state = GameMode.PLAY

        chest = Chest()
        chest.move(2, 6)
        self.game.map.add_entity(chest)
        chest.inventory.append(FireBallStaff())

        # Talk to merchant
        self.game.handle_key_pressed(KeyValues.CHAT)
        self.assertTrue(self.game.waiting_for_friendly_key)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertFalse(self.game.waiting_for_friendly_key)
        self.assertEqual(self.game.state, GameMode.CHEST)
        self.assertTrue(self.game.logs.messages)

        # Navigate in the menu
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.game.handle_key_pressed(KeyValues.LEFT)
        self.assertFalse(self.game.is_in_chest_menu)
        self.game.handle_key_pressed(KeyValues.RIGHT)
        self.assertTrue(self.game.is_in_chest_menu)
        self.game.handle_key_pressed(KeyValues.UP)
        self.assertEqual(self.game.chest_menu.position, 1)

        # The second item is not a heart
        chest.inventory[1] = sword = Sword()
        # Take the second item
        item = self.game.chest_menu.validate()
        self.assertIn(item, chest.inventory)
        self.game.display_actions(DisplayActions.MOUSE, 7, 25,
                                  curses.BUTTON1_CLICKED)
        self.assertIn(item, self.game.player.inventory)
        self.assertNotIn(item, chest.inventory)

        # Give an item back
        self.game.inventory_menu.position = len(self.game.player.inventory) - 1
        self.game.handle_key_pressed(KeyValues.LEFT)
        self.assertFalse(self.game.is_in_chest_menu)
        self.assertIn(sword, self.game.player.inventory)
        self.assertEqual(self.game.inventory_menu.validate(), sword)
        self.game.handle_key_pressed(KeyValues.ENTER)
        self.assertNotIn(sword, self.game.player.inventory)
        self.assertIn(sword, chest.inventory)

        # Test immortality
        self.game.player.hit(chest)
        self.assertTrue(not chest.dead)

        # Exit the menu
        self.game.handle_key_pressed(KeyValues.SPACE)
        self.assertEqual(self.game.state, GameMode.PLAY)

    def test_doors(self) -> None:
        """
        Check that the user can open doors.
        """
        self.game.state = GameMode.PLAY

        self.game.player.move(9, 8)
        self.assertEqual(self.game.map.tiles[10][8], Tile.DOOR)
        # Open door
        self.game.handle_key_pressed(KeyValues.DOWN)
        self.assertEqual(self.game.map.tiles[10][8], Tile.FLOOR)
        self.assertEqual(self.game.player.y, 10)
        self.assertEqual(self.game.player.x, 8)
        self.game.display_actions(DisplayActions.REFRESH)
