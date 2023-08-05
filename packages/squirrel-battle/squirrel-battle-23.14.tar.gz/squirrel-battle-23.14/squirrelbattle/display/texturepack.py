# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import curses
from typing import Any, Tuple, Union


class TexturePack:
    """
    A class to handle displaying several textures.
    """
    _packs = dict()

    name: str
    tile_width: int
    tile_fg_color: Union[int, Tuple[int, int, int]]
    tile_fg_visible_color: Union[int, Tuple[int, int, int]]
    tile_bg_color: Union[int, Tuple[int, int, int]]
    entity_fg_color: Union[int, Tuple[int, int, int]]
    entity_bg_color: Union[int, Tuple[int, int, int]]

    BODY_SNATCH_POTION: str
    BOMB: str
    BOW: str
    CHEST: str
    CHESTPLATE: str
    EAGLE: str
    EMPTY: str
    FIRE_BALL_STAFF: str
    FLOOR: str
    HAZELNUT: str
    HEART: str
    HEDGEHOG: str
    HELMET: str
    MERCHANT: str
    PLAYER: str
    RABBIT: str
    RING_OF_CRITICAL_DAMAGE: str
    RING_OF_MORE_EXPERIENCE: str
    RULER: str
    SCROLL_OF_DAMAGE: str
    SCROLL_OF_WEAKENING: str
    SHIELD: str
    SUNFLOWER: str
    SWORD: str
    TEDDY_BEAR: str
    TIGER: str
    TRUMPET: str
    WALL: str

    ASCII_PACK: "TexturePack"
    SQUIRREL_PACK: "TexturePack"

    def __init__(self, name: str, **kwargs):
        self.name = name
        self.__dict__.update(**kwargs)
        TexturePack._packs[name] = self

    def __getitem__(self, item: str) -> Any:
        return self.__dict__[item]

    @classmethod
    def get_pack(cls, name: str) -> "TexturePack":
        return cls._packs[name.lower()]

    @classmethod
    def get_next_pack_name(cls, name: str) -> str:
        return "squirrel" if name == "ascii" else "ascii"


TexturePack.ASCII_PACK = TexturePack(
    name="ascii",
    tile_width=1,
    tile_fg_visible_color=(1000, 1000, 1000),
    tile_fg_color=curses.COLOR_WHITE,
    tile_bg_color=curses.COLOR_BLACK,
    entity_fg_color=(1000, 1000, 1000),
    entity_bg_color=curses.COLOR_BLACK,

    BODY_SNATCH_POTION='S',
    BOMB='ç',
    BOW=')',
    CHEST='□',
    CHESTPLATE='(',
    DOOR='&',
    EAGLE='µ',
    EMPTY=' ',
    EXPLOSION='%',
    FIRE_BALL_STAFF=':',
    FLOOR='.',
    LADDER='H',
    HAZELNUT='¤',
    HEART='❤',
    HEDGEHOG='*',
    HELMET='0',
    MERCHANT='M',
    MONOCLE='ô',
    PLAYER='@',
    RABBIT='Y',
    RING_OF_CRITICAL_DAMAGE='o',
    RING_OF_MORE_EXPERIENCE='o',
    RULER='\\',
    SHIELD='D',
    SUNFLOWER='I',
    SWORD='\u2020',
    TEDDY_BEAR='8',
    TIGER='n',
    TRUMPET='/',
    WALL='#',
    SCROLL_OF_DAMAGE=']',
    SCROLL_OF_WEAKENING=']',
)

TexturePack.SQUIRREL_PACK = TexturePack(
    name="squirrel",
    tile_width=2,
    tile_fg_visible_color=(1000, 1000, 1000),
    tile_fg_color=curses.COLOR_WHITE,
    tile_bg_color=curses.COLOR_BLACK,
    entity_fg_color=(1000, 1000, 1000),
    entity_bg_color=(1000, 1000, 1000),

    BODY_SNATCH_POTION='🔀',
    BOMB='💣',
    BOW='🏹',
    CHEST='🧰',
    CHESTPLATE='🦺',
    DOOR=('🚪', curses.COLOR_WHITE, (1000, 1000, 1000),
          curses.COLOR_WHITE, (1000, 1000, 1000)),
    EAGLE='🦅',
    EMPTY='  ',
    EXPLOSION='💥',
    FIRE_BALL_STAFF='🪄',
    FLOOR='██',
    LADDER=('🪜', curses.COLOR_WHITE, (1000, 1000, 1000),
            curses.COLOR_WHITE, (1000, 1000, 1000)),
    HAZELNUT='🌰',
    HEART='💜',
    HEDGEHOG='🦔',
    HELMET='⛑️ ',
    PLAYER='🐿️ ️',
    MERCHANT='🦜',
    MONOCLE='🧐',
    RABBIT='🐇',
    RING_OF_CRITICAL_DAMAGE='💍',
    RING_OF_MORE_EXPERIENCE='💍',
    RULER='📏',
    SHIELD='🛡️ ',
    SUNFLOWER='🌻',
    SWORD='🗡️ ',
    TEDDY_BEAR='🧸',
    TIGER='🐅',
    TRUMPET='🎺',
    WALL='🧱',
    SCROLL_OF_DAMAGE='📜',
    SCROLL_OF_WEAKENING='📜',
)
