# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import curses
import json
from json import JSONDecodeError
import os
import sys
from typing import Any, List, Optional

from . import menus
from .entities.player import Player
from .enums import DisplayActions, GameMode, KeyValues
from .interfaces import Logs, Map
from .mapgeneration import broguelike
from .resources import ResourceManager
from .settings import Settings
from .translations import gettext as _, Translator


class Game:
    """
    The game object controls all actions in the game.
    """
    maps: List[Map]
    map_index: int
    player: Player
    screen: Any
    # display_actions is a display interface set by the bootstrapper
    display_actions: callable

    def __init__(self) -> None:
        """
        Initiates the game.
        """
        self.state = GameMode.MAINMENU
        self.waiting_for_friendly_key = False
        self.waiting_for_launch_key = False
        self.is_in_store_menu = True
        self.is_in_chest_menu = True
        self.settings = Settings()
        self.settings.load_settings()
        self.settings.write_settings()
        Translator.setlocale(self.settings.LOCALE)
        self.main_menu = menus.MainMenu()
        self.settings_menu = menus.SettingsMenu()
        self.settings_menu.update_values(self.settings)
        self.inventory_menu = menus.InventoryMenu()
        self.store_menu = menus.StoreMenu()
        self.chest_menu = menus.ChestMenu()
        self.logs = Logs()
        self.message = None

    def new_game(self) -> None:
        """
        Creates a new game on the screen.
        """
        self.maps = []
        self.map_index = 0
        self.map = broguelike.Generator().run()
        self.map.logs = self.logs
        self.logs.clear()
        self.player = Player()
        self.map.add_entity(self.player)
        self.player.move(self.map.start_y, self.map.start_x)
        self.inventory_menu.update_player(self.player)

    @property
    def map(self) -> Map:
        """
        Return the current map where the user is.
        """
        return self.maps[self.map_index]

    @map.setter
    def map(self, m: Map) -> None:
        """
        Redefine the current map.
        """
        if len(self.maps) == self.map_index:
            # Insert new map
            self.maps.append(m)
        # Redefine the current map
        self.maps[self.map_index] = m

    def run(self, screen: Any) -> None:  # pragma no cover
        """
        Main infinite loop.
        We wait for the player's action, then we do what should be done
        when a key gets pressed.
        """
        screen.refresh()
        while True:
            screen.erase()
            screen.noutrefresh()
            self.display_actions(DisplayActions.REFRESH)
            curses.doupdate()
            try:
                key = screen.getkey()
            except KeyboardInterrupt:
                exit(0)
                return
            if key == "KEY_MOUSE":
                _ignored1, x, y, _ignored2, attr = curses.getmouse()
                self.display_actions(DisplayActions.MOUSE, y, x, attr)
            else:
                self.handle_key_pressed(
                    KeyValues.translate_key(key, self.settings), key)

    def handle_key_pressed(self, key: Optional[KeyValues], raw_key: str = '')\
            -> None:
        """
        Indicates what should be done when a given key is pressed,
        according to the current game state.
        """
        if self.message:
            self.message = None
            self.display_actions(DisplayActions.REFRESH)
            return

        if self.state == GameMode.PLAY:
            if self.waiting_for_friendly_key:
                # The player requested to talk with a friendly entity
                self.handle_friendly_entity_chat(key)
            elif self.waiting_for_launch_key:
                # The player requested to launch
                self.handle_launch(key)
            else:
                self.handle_key_pressed_play(key)
        elif self.state == GameMode.INVENTORY:
            self.handle_key_pressed_inventory(key)
        elif self.state == GameMode.MAINMENU:
            self.handle_key_pressed_main_menu(key)
        elif self.state == GameMode.SETTINGS:
            self.settings_menu.handle_key_pressed(key, raw_key, self)
        elif self.state == GameMode.STORE:
            self.handle_key_pressed_store(key)
        elif self.state == GameMode.CHEST:
            self.handle_key_pressed_chest(key)
        elif self.state == GameMode.CREDITS:
            self.state = GameMode.MAINMENU
        self.display_actions(DisplayActions.REFRESH)

    def handle_key_pressed_play(self, key: KeyValues) -> None:  # noqa: C901
        """
        In play mode, arrows or zqsd move the main character.
        """
        if key == KeyValues.UP:
            if self.player.move_up():
                self.map.tick(self.player)
        elif key == KeyValues.DOWN:
            if self.player.move_down():
                self.map.tick(self.player)
        elif key == KeyValues.LEFT:
            if self.player.move_left():
                self.map.tick(self.player)
        elif key == KeyValues.RIGHT:
            if self.player.move_right():
                self.map.tick(self.player)
        elif key == KeyValues.INVENTORY:
            self.state = GameMode.INVENTORY
            self.display_actions(DisplayActions.UPDATE)
        elif key == KeyValues.USE and self.player.equipped_main:
            if self.player.equipped_main:
                self.player.equipped_main.use()
            if self.player.equipped_secondary:
                self.player.equipped_secondary.use()
        elif key == KeyValues.LAUNCH:
            # Wait for the direction to launch in
            self.waiting_for_launch_key = True
        elif key == KeyValues.SPACE:
            self.state = GameMode.MAINMENU
        elif key == KeyValues.CHAT:
            # Wait for the direction of the friendly entity
            self.waiting_for_friendly_key = True
        elif key == KeyValues.WAIT:
            self.map.tick(self.player)
        elif key == KeyValues.LADDER:
            self.handle_ladder()
        elif key == KeyValues.DANCE:
            self.player.dance()
            self.map.tick(self.player)

    def handle_ladder(self) -> None:
        """
        The player pressed the ladder key to switch map
        """
        # On a ladder, we switch level
        y, x = self.player.y, self.player.x
        if not self.map.tiles[y][x].is_ladder():
            return

        # We move up on the ladder of the beginning,
        # down at the end of the stage
        move_down = y != self.map.start_y and x != self.map.start_x
        old_map = self.map
        self.map_index += 1 if move_down else -1
        if self.map_index == -1:
            self.map_index = 0
            return
        while self.map_index >= len(self.maps):
            m = broguelike.Generator().run()
            m.logs = self.logs
            self.maps.append(m)
        new_map = self.map
        new_map.floor = self.map_index
        old_map.remove_entity(self.player)
        new_map.add_entity(self.player)
        if move_down:
            self.player.move(self.map.start_y, self.map.start_x)
            self.logs.add_message(
                _("The player climbs down to the floor {floor}.")
                .format(floor=-self.map_index))
        else:
            # Find the ladder of the end of the game
            ladder_y, ladder_x = -1, -1
            for y in range(self.map.height):
                for x in range(self.map.width):
                    if (y, x) != (self.map.start_y, self.map.start_x) \
                            and self.map.tiles[y][x].is_ladder():
                        ladder_y, ladder_x = y, x
                        break
            self.player.move(ladder_y, ladder_x)
            self.logs.add_message(
                _("The player climbs up the floor {floor}.")
                .format(floor=-self.map_index))

        self.display_actions(DisplayActions.UPDATE)

    def handle_friendly_entity_chat(self, key: KeyValues) -> None:
        """
        If the player tries to talk to a friendly entity, the game waits for
        a directional key to be pressed, verifies there is a friendly entity
        in that direction and then lets the player interact with it.
        """
        if not self.waiting_for_friendly_key:
            return
        self.waiting_for_friendly_key = False

        if key == KeyValues.UP:
            xp = self.player.x
            yp = self.player.y - 1
        elif key == KeyValues.DOWN:
            xp = self.player.x
            yp = self.player.y + 1
        elif key == KeyValues.LEFT:
            xp = self.player.x - 1
            yp = self.player.y
        elif key == KeyValues.RIGHT:
            xp = self.player.x + 1
            yp = self.player.y
        else:
            return
        if self.map.entity_is_present(yp, xp):
            for entity in self.map.entities:
                if entity.is_friendly() and entity.x == xp and \
                        entity.y == yp:
                    msg = entity.talk_to(self.player)
                    self.logs.add_message(msg)
                    if entity.is_merchant():
                        self.state = GameMode.STORE
                        self.is_in_store_menu = True
                        self.store_menu.update_merchant(entity)
                        self.display_actions(DisplayActions.UPDATE)
                    elif entity.is_chest():
                        self.state = GameMode.CHEST
                        self.is_in_chest_menu = True
                        self.chest_menu.update_chest(entity)
                        self.display_actions(DisplayActions.UPDATE)

    def handle_launch(self, key: KeyValues) -> None:
        """
        If the player tries to throw something in a direction, the game looks
        for entities in that direction and within the range of the player's
        weapon and adds damage
        """
        if not self.waiting_for_launch_key:
            return
        self.waiting_for_launch_key = False

        if key == KeyValues.UP:
            direction = 0
        elif key == KeyValues.DOWN:
            direction = 2
        elif key == KeyValues.LEFT:
            direction = 3
        elif key == KeyValues.RIGHT:
            direction = 1
        else:
            return

        if self.player.equipped_main:
            if self.player.equipped_main.throw(direction):
                self.map.tick(self.player)

    def handle_key_pressed_inventory(self, key: KeyValues) -> None:
        """
        In the inventory menu, we can interact with items or close the menu.
        """
        if key == KeyValues.SPACE or key == KeyValues.INVENTORY:
            self.state = GameMode.PLAY
        elif key == KeyValues.UP:
            self.inventory_menu.go_up()
        elif key == KeyValues.DOWN:
            self.inventory_menu.go_down()
        if self.inventory_menu.values and not self.player.dead:
            if key == KeyValues.USE:
                self.inventory_menu.validate().use()
            elif key == KeyValues.EQUIP:
                item = self.inventory_menu.validate()
                item.unequip() if item.equipped else item.equip()
            elif key == KeyValues.DROP:
                self.inventory_menu.validate().drop()

            # Ensure that the cursor has a good position
            self.inventory_menu.position = min(self.inventory_menu.position,
                                               len(self.inventory_menu.values)
                                               - 1)

    def handle_key_pressed_store(self, key: KeyValues) -> None:
        """
        In a store menu, we can buy items or close the menu.
        """
        menu = self.store_menu if self.is_in_store_menu else self.inventory_menu

        if key == KeyValues.SPACE or key == KeyValues.INVENTORY:
            self.state = GameMode.PLAY
        elif key == KeyValues.UP:
            menu.go_up()
        elif key == KeyValues.DOWN:
            menu.go_down()
        elif key == KeyValues.LEFT:
            self.is_in_store_menu = False
            self.display_actions(DisplayActions.UPDATE)
        elif key == KeyValues.RIGHT:
            self.is_in_store_menu = True
            self.display_actions(DisplayActions.UPDATE)
        if menu.values and not self.player.dead:
            if key == KeyValues.ENTER:
                item = menu.validate()
                owner = self.store_menu.merchant if self.is_in_store_menu \
                    else self.player
                buyer = self.player if self.is_in_store_menu \
                    else self.store_menu.merchant
                flag = item.be_sold(buyer, owner)
                if not flag:
                    self.message = _("The buyer does not have enough money")
                self.display_actions(DisplayActions.UPDATE)
            # Ensure that the cursor has a good position
            menu.position = min(menu.position, len(menu.values) - 1)

    def handle_key_pressed_chest(self, key: KeyValues) -> None:
        """
        In a chest menu, we can take or put items or close the menu.
        """
        menu = self.chest_menu if self.is_in_chest_menu else self.inventory_menu

        if key == KeyValues.SPACE or key == KeyValues.INVENTORY:
            self.state = GameMode.PLAY
        elif key == KeyValues.UP:
            menu.go_up()
        elif key == KeyValues.DOWN:
            menu.go_down()
        elif key == KeyValues.LEFT:
            self.is_in_chest_menu = False
            self.display_actions(DisplayActions.UPDATE)
        elif key == KeyValues.RIGHT:
            self.is_in_chest_menu = True
            self.display_actions(DisplayActions.UPDATE)
        if menu.values and not self.player.dead:
            if key == KeyValues.ENTER:
                item = menu.validate()
                owner = self.chest_menu.chest if self.is_in_chest_menu \
                    else self.player
                buyer = self.player if self.is_in_chest_menu \
                    else self.chest_menu.chest
                item.be_sold(buyer, owner, for_free=True)
                self.display_actions(DisplayActions.UPDATE)
            # Ensure that the cursor has a good position
            menu.position = min(menu.position, len(menu.values) - 1)

    def handle_key_pressed_main_menu(self, key: KeyValues) -> None:
        """
        In the main menu, we can navigate through different options.
        """
        if key == KeyValues.DOWN:
            self.main_menu.go_down()
        if key == KeyValues.UP:
            self.main_menu.go_up()
        if key == KeyValues.ENTER:
            option = self.main_menu.validate()
            if option == menus.MainMenuValues.START:
                self.new_game()
                self.display_actions(DisplayActions.UPDATE)
                self.state = GameMode.PLAY
            if option == menus.MainMenuValues.RESUME:
                self.state = GameMode.PLAY
            elif option == menus.MainMenuValues.SAVE:
                self.save_game()
            elif option == menus.MainMenuValues.LOAD:
                self.load_game()
            elif option == menus.MainMenuValues.SETTINGS:
                self.state = GameMode.SETTINGS
            elif option == menus.MainMenuValues.EXIT:
                sys.exit(0)

    def save_state(self) -> dict:
        """
        Saves the game to a dictionary.
        """
        return dict(map_index=self.map_index,
                    maps=[m.save_state() for m in self.maps])

    def load_state(self, d: dict) -> None:
        """
        Loads the game from a dictionary.
        """
        try:
            self.map_index = d["map_index"]
            self.maps = [Map().load_state(map_dict) for map_dict in d["maps"]]
            for i, m in enumerate(self.maps):
                m.floor = i
                m.logs = self.logs
        except KeyError as error:
            self.message = _("Some keys are missing in your save file.\n"
                             "Your save seems to be corrupt. It got deleted.")\
                + f"\n{error}"
            os.unlink(ResourceManager.get_config_path("save.json"))
            self.display_actions(DisplayActions.UPDATE)
            return

        players = self.map.find_entities(Player)
        if not players:
            self.message = _("No player was found on this map!\n"
                             "Maybe you died?")
            self.player.health = 0
            self.display_actions(DisplayActions.UPDATE)
            return

        self.player = players[0]
        self.inventory_menu.update_player(self.player)
        self.map.compute_visibility(self.player.y, self.player.x,
                                    self.player.vision)
        self.display_actions(DisplayActions.UPDATE)

    def load_game(self) -> None:
        """
        Loads the game from a file.
        """
        file_path = ResourceManager.get_config_path("save.json")
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                try:
                    state = json.loads(f.read())
                    self.load_state(state)
                except JSONDecodeError:
                    self.message = _("The JSON file is not correct.\n"
                                     "Your save seems corrupted. "
                                     "It got deleted.")
                    os.unlink(file_path)
                    self.display_actions(DisplayActions.UPDATE)

    def save_game(self) -> None:
        """
        Saves the game to a file.
        """
        with open(ResourceManager.get_config_path("save.json"), "w") as f:
            f.write(json.dumps(self.save_state()))
