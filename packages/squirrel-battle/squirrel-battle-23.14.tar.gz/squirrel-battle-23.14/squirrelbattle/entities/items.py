# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

from random import choice, randint
from typing import Any, Optional

from ..interfaces import Entity, FightingEntity, InventoryHolder, Map
from ..translations import gettext as _


class Item(Entity):
    """
    A class for items.
    """
    held_by: Optional[InventoryHolder]
    price: int

    def __init__(self, equipped: bool = False,
                 held_by: Optional[InventoryHolder] = None,
                 hold_slot: str = "equipped_secondary",
                 price: int = 2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.held_by = held_by
        self.equipped = equipped
        self.hold_slot = hold_slot
        if equipped:
            self.equip()
        self.price = price

    @property
    def description(self) -> str:
        """
        In the inventory, indicate the usefulness of the item.
        """
        return ""

    def drop(self) -> None:
        """
        The item is dropped from the inventory onto the floor.
        """
        if self.held_by is not None:
            self.unequip()
            self.held_by.remove_from_inventory(self)
            self.held_by.map.add_entity(self)
            self.move(self.held_by.y, self.held_by.x)
            self.held_by = None

    def use(self) -> None:
        """
        Indicates what should be done when the item is used.
        """

    def throw(self, direction: int) -> Any:
        """
        Indicates what should be done when the item is thrown.
        """

    def on_equip(self) -> None:
        """
        Indicates a special behaviour when equipping
        """

    def on_unequip(self) -> None:
        """
        Indicates a special behaviour when unequipping
        """

    def equip(self) -> None:
        """
        Indicates what should be done when the item is equipped.
        """
        # Other objects are only equipped as secondary.
        if not self.equipped:
            if getattr(self.held_by, self.hold_slot):
                getattr(self.held_by, self.hold_slot).unequip()
            self.equipped = True
            setattr(self.held_by, self.hold_slot, self)
            self.on_equip()

    def unequip(self) -> None:
        """
        Indicates what should be done when the item is unequipped.
        """
        if self.equipped:
            setattr(self.held_by, self.hold_slot, None)
            self.equipped = False
            self.on_unequip()

    def hold(self, holder: InventoryHolder) -> None:
        """
        The item is taken from the floor and put into the inventory.
        """
        self.held_by = holder
        self.held_by.map.remove_entity(self)
        holder.add_to_inventory(self)

    def save_state(self) -> dict:
        """
        Saves the state of the item into a dictionary.
        """
        d = super().save_state()
        d["equipped"] = self.equipped
        return d

    @staticmethod
    def get_all_items() -> list:
        """
        Returns the list of all item classes.
        """
        return [BodySnatchPotion, Bomb, Bow, Chestplate, FireBallStaff,
                Heart, Helmet, Monocle, ScrollofDamage, ScrollofWeakening,
                Shield, Sword, RingCritical, RingXP, Ruler]

    def be_sold(self, buyer: InventoryHolder, seller: InventoryHolder,
                for_free: bool = False) -> bool:
        """
        Does all necessary actions when an object is to be sold.
        Is overwritten by some classes that cannot exist in the player's
        inventory.
        """
        if for_free:
            self.unequip() if self.equipped else None
            self.hold(buyer)
            seller.remove_from_inventory(self)
            return True
        elif buyer.hazel >= self.price:
            self.unequip() if self.equipped else None
            self.hold(buyer)
            seller.remove_from_inventory(self)
            buyer.change_hazel_balance(-self.price)
            seller.change_hazel_balance(self.price)
            return True
        else:
            return False


class Heart(Item):
    """
    A heart item to return health to the player.
    """
    healing: int

    def __init__(self, name: str = "heart", healing: int = 5, price: int = 3,
                 *args, **kwargs):
        super().__init__(name=name, price=price, *args, **kwargs)
        self.healing = healing

    @property
    def description(self) -> str:
        return f"HP+{self.healing}"

    def hold(self, entity: InventoryHolder) -> None:
        """
        When holding a heart, the player is healed and
        the item is not put in the inventory.
        """
        entity.health = min(entity.maxhealth, entity.health + self.healing)
        entity.map.remove_entity(self)

    def save_state(self) -> dict:
        """
        Saves the state of the heart into a dictionary.
        """
        d = super().save_state()
        d["healing"] = self.healing
        return d


class Bomb(Item):
    """
    A bomb item intended to deal damage to enemies at long range
    """
    damage: int = 5
    exploding: bool
    owner: Optional["InventoryHolder"]
    tick: int

    def __init__(self, name: str = "bomb", damage: int = 5,
                 exploding: bool = False, price: int = 4, *args, **kwargs):
        super().__init__(name=name, price=price, *args, **kwargs)
        self.damage = damage
        self.exploding = exploding
        self.tick = 4
        self.owner = None

    def use(self) -> None:
        """
        When the bomb is used, it is thrown and then it explodes.
        """
        if self.held_by is not None:
            self.owner = self.held_by
            super().drop()
            self.exploding = True

    def act(self, m: Map) -> None:
        """
        Special exploding action of the bomb.
        """
        if self.exploding:
            if self.tick > 0:
                # The bomb will explode in <tick> moves
                self.tick -= 1
            else:
                # The bomb is exploding.
                # Each entity that is close to the bomb takes damages.
                # The player earn XP if the entity was killed.
                log_message = _("Bomb is exploding.")
                for e in m.entities.copy():
                    if abs(e.x - self.x) + abs(e.y - self.y) <= 3 and \
                            isinstance(e, FightingEntity):
                        log_message += " " + e.take_damage(self, self.damage)
                        if e.dead:
                            self.owner.add_xp(randint(3, 7))
                m.logs.add_message(log_message)
                m.entities.remove(self)

                # Add sparkles where the bomb exploded.
                explosion = Explosion(y=self.y, x=self.x)
                self.map.add_entity(explosion)

    def save_state(self) -> dict:
        """
        Saves the state of the bomb into a dictionary.
        """
        d = super().save_state()
        d["exploding"] = self.exploding
        d["damage"] = self.damage
        return d


class Explosion(Item):
    """
    When a bomb explodes, the explosion is displayed.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(name="explosion", *args, **kwargs)

    def act(self, m: Map) -> None:
        """
        The bomb disappears after exploding.
        """
        m.remove_entity(self)

    def hold(self, player: InventoryHolder) -> None:
        """
        The player can't hold an explosion.
        """


class Weapon(Item):
    """
    Non-throwable items that improve player damage
    """
    damage: int

    def __init__(self, damage: int = 3, *args, **kwargs):
        super().__init__(hold_slot="equipped_main", *args, **kwargs)
        self.damage = damage

    @property
    def description(self) -> str:
        return f"STR+{self.damage}" if self.damage else super().description

    def save_state(self) -> dict:
        """
        Saves the state of the weapon into a dictionary
        """
        d = super().save_state()
        d["damage"] = self.damage
        return d

    def on_equip(self) -> None:
        """
        When a weapon is equipped, the player gains strength.
        """
        self.held_by.strength += self.damage

    def on_unequip(self) -> None:
        """
        Remove the strength earned by the weapon.
        :return:
        """
        self.held_by.strength -= self.damage


class Sword(Weapon):
    """
    A basic weapon
    """
    def __init__(self, name: str = "sword", price: int = 20,
                 *args, **kwargs):
        super().__init__(name=name, price=price, *args, **kwargs)


class Ruler(Weapon):
    """
    A basic weapon
    """
    def __init__(self, name: str = "ruler", price: int = 2,
                 damage: int = 1, *args, **kwargs):
        super().__init__(name=name, price=price, damage=damage, *args, **kwargs)


class Armor(Item):
    """
    Class of items that increase the player's constitution.
    """
    constitution: int

    def __init__(self, constitution: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.constitution = constitution

    @property
    def description(self) -> str:
        return f"CON+{self.constitution}" if self.constitution \
            else super().description

    def on_equip(self) -> None:
        self.held_by.constitution += self.constitution

    def on_unequip(self) -> None:
        self.held_by.constitution -= self.constitution

    def save_state(self) -> dict:
        d = super().save_state()
        d["constitution"] = self.constitution
        return d


class Shield(Armor):
    """
    Class of shield items, they can be equipped in the other hand.
    """
    def __init__(self, name: str = "shield", constitution: int = 2,
                 price: int = 16, *args, **kwargs):
        super().__init__(name=name, constitution=constitution, price=price,
                         *args, **kwargs)


class Helmet(Armor):
    """
    Class of helmet items, they can be equipped on the head.
    """
    def __init__(self, name: str = "helmet", constitution: int = 2,
                 price: int = 18, *args, **kwargs):
        super().__init__(name=name, constitution=constitution, price=price,
                         hold_slot="equipped_helmet", *args, **kwargs)


class Chestplate(Armor):
    """
    Class of chestplate items, they can be equipped on the body.
    """
    def __init__(self, name: str = "chestplate", constitution: int = 4,
                 price: int = 30, *args, **kwargs):
        super().__init__(name=name, constitution=constitution, price=price,
                         hold_slot="equipped_armor", *args, **kwargs)


class BodySnatchPotion(Item):
    """
    The body-snatch potion allows to exchange all characteristics with a random
    other entity.
    """

    def __init__(self, name: str = "body_snatch_potion", price: int = 14,
                 *args, **kwargs):
        super().__init__(name=name, price=price, *args, **kwargs)

    def use(self) -> None:
        """
        Find a valid random entity, then exchange characteristics.
        """
        valid_entities = self.held_by.map.find_entities(FightingEntity)
        valid_entities.remove(self.held_by)
        entity = choice(valid_entities)
        entity_state = entity.save_state()
        player_state = self.held_by.save_state()
        self.held_by.__dict__.update(entity_state)
        entity.__dict__.update(player_state)
        self.held_by.map.currenty, self.held_by.map.currentx = self.held_by.y,\
            self.held_by.x

        self.held_by.map.logs.add_message(
            _("{player} exchanged its body with {entity}.").format(
                player=self.held_by.translated_name.capitalize(),
                entity=entity.translated_name))

        self.held_by.recalculate_paths()

        self.held_by.inventory.remove(self)


class Ring(Item):
    """
    A class of rings that boost the player's statistics.
    """
    maxhealth: int
    strength: int
    intelligence: int
    charisma: int
    dexterity: int
    constitution: int
    critical: int
    experience: float

    def __init__(self, maxhealth: int = 0, strength: int = 0,
                 intelligence: int = 0, charisma: int = 0,
                 dexterity: int = 0, constitution: int = 0,
                 critical: int = 0, experience: float = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxhealth = maxhealth
        self.strength = strength
        self.intelligence = intelligence
        self.charisma = charisma
        self.dexterity = dexterity
        self.constitution = constitution
        self.critical = critical
        self.experience = experience

    @property
    def description(self) -> str:
        fields = [("MAX HP", self.maxhealth), ("STR", self.strength),
                  ("INT", self.intelligence), ("CHR", self.charisma),
                  ("DEX", self.dexterity), ("CON", self.constitution),
                  ("CRI", self.critical), ("XP", self.experience)]
        return ", ".join(f"{key}+{value}" for key, value in fields if value)

    def on_equip(self) -> None:
        self.held_by.maxhealth += self.maxhealth
        self.held_by.strength += self.strength
        self.held_by.intelligence += self.intelligence
        self.held_by.charisma += self.charisma
        self.held_by.dexterity += self.dexterity
        self.held_by.constitution += self.constitution
        self.held_by.critical += self.critical
        self.held_by.xp_buff += self.experience

    def on_unequip(self) -> None:
        self.held_by.maxhealth -= self.maxhealth
        self.held_by.strength -= self.strength
        self.held_by.intelligence -= self.intelligence
        self.held_by.charisma -= self.charisma
        self.held_by.dexterity -= self.dexterity
        self.held_by.constitution -= self.constitution
        self.held_by.critical -= self.critical
        self.held_by.xp_buff -= self.experience

    def save_state(self) -> dict:
        d = super().save_state()
        d["maxhealth"] = self.maxhealth
        d["strength"] = self.strength
        d["intelligence"] = self.intelligence
        d["charisma"] = self.charisma
        d["dexterity"] = self.dexterity
        d["constitution"] = self.constitution
        d["critical"] = self.critical
        d["experience"] = self.experience
        return d


class RingCritical(Ring):
    def __init__(self, name: str = "ring_of_critical_damage", price: int = 15,
                 critical: int = 20, *args, **kwargs):
        super().__init__(name=name, price=price, critical=critical,
                         *args, **kwargs)


class RingXP(Ring):
    def __init__(self, name: str = "ring_of_more_experience", price: int = 25,
                 experience: float = 2, *args, **kwargs):
        super().__init__(name=name, price=price, experience=experience,
                         *args, **kwargs)


class ScrollofDamage(Item):
    """
    A scroll that, when used, deals damage to all entities in a certain radius.
    """
    def __init__(self, name: str = "scroll_of_damage", price: int = 18,
                 *args, **kwargs):
        super().__init__(name=name, price=price, *args, **kwargs)

    def use(self) -> None:
        """
        Find all entities within a radius of 5, and deal damage based on the
        player's intelligence.
        """
        for entity in self.held_by.map.entities:
            if entity.is_fighting_entity() and not entity == self.held_by:
                if entity.distance(self.held_by) <= 5:
                    self.held_by.map.logs.add_message(entity.take_damage(
                        self.held_by, self.held_by.intelligence))
        self.held_by.inventory.remove(self)


class ScrollofWeakening(Item):
    """
    A scroll that, when used, reduces the damage of the ennemies for 3 turns.
    """
    def __init__(self, name: str = "scroll_of_weakening", price: int = 13,
                 *args, **kwargs):
        super().__init__(name=name, price=price, *args, **kwargs)

    def use(self) -> None:
        """
        Find all entities and reduce their damage.
        """
        for entity in self.held_by.map.entities:
            if entity.is_fighting_entity() and not entity == self.held_by:
                entity.strength = entity.strength - \
                    max(1, self.held_by.intelligence // 2)
                entity.effects.append(["strength",
                                       -max(1, self.held_by.intelligence // 2),
                                       3])
        self.held_by.map.logs.add_message(
            _(f"The ennemies have -{max(1, self.held_by.intelligence // 2)}"
              + "strength for 3 turns"))
        self.held_by.inventory.remove(self)


class LongRangeWeapon(Weapon):
    def __init__(self, damage: int = 4,
                 rang: int = 3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = damage
        self.range = rang

    def throw(self, direction: int) -> Any:
        to_kill = None
        for entity in self.held_by.map.entities:
            if entity.is_fighting_entity():
                if direction == 0 and self.held_by.x == entity.x \
                    and self.held_by.y - entity.y > 0 and \
                        self.held_by.y - entity.y <= self.range:
                    to_kill = entity
                elif direction == 2 and self.held_by.x == entity.x \
                    and entity.y - self.held_by.y > 0 and \
                        entity.y - self.held_by.y <= self.range:
                    to_kill = entity
                elif direction == 1 and self.held_by.y == entity.y \
                    and entity.x - self.held_by.x > 0 and \
                        entity.x - self.held_by.x <= self.range:
                    to_kill = entity
                elif direction == 3 and self.held_by.y == entity.y \
                    and self.held_by.x - entity.x > 0 and \
                        self.held_by.x - entity.x <= self.range:
                    to_kill = entity
        if to_kill:
            line = _("{name}").format(name=to_kill.translated_name.capitalize()
                                      ) + self.string + " "\
                                        + to_kill.take_damage(
                                            self.held_by, self.damage
                                            + getattr(self.held_by, self.stat))
            self.held_by.map.logs.add_message(line)
        return (to_kill.y, to_kill.x) if to_kill else None

    @property
    def stat(self) -> str:
        """
        The stat that is used when using the object: dexterity for a bow
        or intelligence for a magic staff.
        """

    @property
    def string(self) -> str:
        """
        The string that is printed when we hit an ennemy.
        """


class Bow(LongRangeWeapon):
    """
    A type of long range weapon that deals damage
    based on the player's dexterity
    """
    def __init__(self, name: str = "bow", price: int = 22, damage: int = 4,
                 rang: int = 3, *args, **kwargs):
        super().__init__(name=name, price=price, damage=damage,
                         rang=rang, *args, **kwargs)

    @property
    def stat(self) -> str:
        """
        Here it is dexterity
        """
        return "dexterity"

    @property
    def string(self) -> str:
        return _(" is shot by an arrow.")


class FireBallStaff(LongRangeWeapon):
    """
    A type of powerful long range weapon that deals damage
    based on the player's intelligence
    """
    def __init__(self, name: str = "fire_ball_staff", price: int = 36,
                 damage: int = 6, rang: int = 4, *args, **kwargs):
        super().__init__(name=name, price=price, damage=damage,
                         rang=rang, *args, **kwargs)

    @property
    def stat(self) -> str:
        """
        Here it is intelligence
        """
        return "intelligence"

    @property
    def string(self) -> str:
        return _(" is shot by a fire ball.")

    def throw(self, direction: int) -> Any:
        """
        Adds an explosion animation when killing something.
        """
        coord = super().throw(direction)
        if coord:
            y = coord[0]
            x = coord[1]

            explosion = Explosion(y=y, x=x)
            self.held_by.map.add_entity(explosion)
            return y, x


class Monocle(Item):
    def __init__(self, name: str = "monocle", price: int = 10,
                 *args, **kwargs):
        super().__init__(name=name, price=price, *args, **kwargs)
