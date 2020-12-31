from datetime import datetime, timedelta

from sqlalchemy import Column, Table, Integer, String, Text, BigInteger, ForeignKey, DateTime, Interval, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from utils import occurrence
from math import floor

"""Character automated HP generation variables"""
HP_GEN_AMOUNT = 10
HP_GEN_INTERVAL = 600  # 600 seconds is equivalent to 10 minutes

Base = declarative_base()

"""" Association tables """
character_attribute = Table(
    'character_attributes',
    Base.metadata,
    Column('character_id', ForeignKey('characters.id'), primary_key=True),
    Column('attribute_id', ForeignKey('attributes.id'), primary_key=True)
)

character_location = Table(
    'character_locations',
    Base.metadata,
    Column('character_id', ForeignKey('characters.id'), primary_key=True),
    Column('location_id', ForeignKey('locations.id'), primary_key=True)
)

item_attribute = Table(
    'item_attributes',
    Base.metadata,
    Column('item_id', ForeignKey('items.id'), primary_key=True),
    Column('attribute_id', ForeignKey('attributes.id'), primary_key=True)
)

entity_attribute = Table(
    'entity_attributes',
    Base.metadata,
    Column('entity_id', ForeignKey('entities.id'), primary_key=True),
    Column('attribute_id', ForeignKey('attributes.id'), primary_key=True)
)

entity_location = Table(
    'entity_locations',
    Base.metadata,
    Column('entity_id', ForeignKey('entities.id'), primary_key=True),
    Column('location_id', ForeignKey('locations.id'), primary_key=True)
)

"""

Classes

"""


# DONE
class User(Base):
    """User class"""

    __tablename__ = 'users'

    _id = Column('id', Integer, primary_key=True)
    discord_id = Column(BigInteger, unique=True)
    init_roll = Column(Integer)
    _last_online = Column('last_online', DateTime, default=func.now(), onupdate=func.now())

    character = relationship('Character', back_populates='user', uselist=False)

    def __repr__(self):
        return "<User(discord_id='{}' init_roll='{}')>".format(self.discord_id, self.init_roll)


# DONE
class Attribute(Base):
    """Attribute class"""

    __tablename__ = 'attributes'

    _id = Column('id', Integer, primary_key=True)
    hp = Column(Integer)
    strength = Column(Integer)
    defense = Column(Integer)

    def __repr__(self):
        return "<Attribute(hp='{}', strength='{}', defense='{}')>".format(
            self.hp, self.strength, self.defense
        )


# DONE
class Character(Base):
    """Character class"""

    __tablename__ = 'characters'

    _id = Column('id', Integer, primary_key=True)
    _user_id = Column('user_id', Integer, ForeignKey('users.id'))
    level = Column(Integer)
    exp = Column(Integer)
    _current_hp = Column('current_hp', Integer)
    money = Column(Integer)
    _hp_last_updated = Column('hp_last_updated', DateTime, default=func.now())

    # relations
    attribute = relationship('Attribute', secondary=character_attribute, uselist=False)
    user = relationship('User', back_populates='character', uselist=False)
    items = relationship('CharacterItem', back_populates='character')
    equipments = relationship('CharacterEquipment', back_populates='character')
    location = relationship('Location', secondary=character_location, back_populates='characters', uselist=False)
    companions = relationship('CharacterCompanion')

    def is_full_hp(self):
        return self.current_hp == self.max_hp

    def is_alive(self):
        return self.current_hp > 0

    @hybrid_property
    def current_hp(self):
        if self._current_hp and self.max_hp:  # if max hp is not None
            if self._current_hp < self.max_hp:
                regen = occurrence(self._hp_last_updated, HP_GEN_INTERVAL) * HP_GEN_AMOUNT
                self._current_hp += regen
                if self._current_hp > self.max_hp:  # if current hp exceeds the max hp
                    self._current_hp = self.max_hp  # set the current hp value as max hp
        return self._current_hp

    @current_hp.setter
    def current_hp(self, value):
        if self.max_hp:  # if max hp is not None
            if value > self.max_hp:
                raise ValueError('Value exceeds the max_hp')

            if self.is_full_hp():  # condition first if value is full hp
                if value < self.max_hp:  # condition if the new value is is not full hp
                    self._hp_last_updated = datetime.now()

        self._current_hp = value

    @hybrid_property
    def max_hp(self):
        if self.attribute:
            return self.attribute.hp
        else:
            return None

    @max_hp.setter
    def max_hp(self, value):
        if not self.attribute:
            self.attribute = Attribute()
        self.attribute.hp = value

    @hybrid_property
    def strength(self):
        if self.attribute:
            return self.attribute.strength
        else:
            return None

    @strength.setter
    def strength(self, value):
        if not self.attribute:
            self.attribute = Attribute()
        self.attribute.strength = value

    @hybrid_property
    def defense(self):
        if self.attribute:
            return self.attribute.defense
        else:
            return None

    @defense.setter
    def defense(self, value):
        if not self.attribute:
            self.attribute = Attribute()
        self.attribute.defense = value

    def next_level_exp(self):
        base_exp = 200
        return floor(base_exp * (self.level ** 1.2))

    def __level_up(self):
        """Scales the stats in every up of level"""
        stat_growth = 1.5
        self.level += 1
        self.strength += floor(stat_growth * self.level)
        self.defense += floor(stat_growth * self.level)

    def add_exp(self, value):
        self.exp += value

        while self.exp >= self.next_level_exp():
            # value = next_level_exp(self.level) - value
            self.exp -= self.next_level_exp()
            self.__level_up()

    def __repr__(self):
        return "<Character(level='{}', exp='{}', current_hp='{}', money='{}')>".format(
            self.level, self.exp, self.current_hp, self.money
        )


# DONE
class ItemType(Base):
    """
    ItemType class

    Available:
        consumable,
        raw,
        gear
    """

    __tablename__ = 'item_types'

    _id = Column('id', Integer, primary_key=True)
    name = Column(String(10), unique=True)

    items = relationship('Item', back_populates='item_type')

    def __repr__(self):
        return "<ItemType(name='{}')>".format(self.name)


# DONE
class Item(Base):
    """Item class"""

    __tablename__ = 'items'

    _id = Column('id', Integer, primary_key=True)
    _item_type_id = Column('item_type_id', Integer, ForeignKey('item_types.id'))
    name = Column(String(10), unique=True)
    description = Column(Text)
    duration = Column(Interval, default=timedelta())

    item_type = relationship('ItemType', back_populates='items', uselist=False)
    attribute = relationship('Attribute', secondary=item_attribute, uselist=False)

    def __repr__(self):
        return "<Item(name='{}', description='{}', duration='{}')>".format(
            self.name, self.description, self.duration
        )


# DONE
class CharacterItem(Base):
    """CharacterItem class"""

    __tablename__ = 'character_items'

    _character_id = Column('character_id', Integer, ForeignKey('characters.id'), primary_key=True)
    _item_id = Column('item_id', Integer, ForeignKey('items.id'), primary_key=True)
    amount = Column(Integer)

    character = relationship('Character', back_populates='items', uselist=False)
    item = relationship('Item')

    def __repr__(self):
        return "<CharacterItem(item='{}', amount='{}')>".format(
            self.item, self.amount
        )


# NOT CONNECTED TO THE CHARACTER
# DONE
class ShopType(Base):
    """
    ShopType class

    Types:
        Common
        Exclusive
    """

    __tablename__ = 'shop_types'

    _id = Column('id', Integer, primary_key=True)
    name = Column(String(20), unique=True)

    def __repr__(self):
        return "<ShopType(name='{}')>".format(
            self.name
        )


# NOT CONNECTED TO THE CHARACTER
# DONE
class ShopItem(Base):
    """ShopItem class"""

    __tablename__ = 'shop_items'

    _id = Column('id', Integer, primary_key=True)
    _item_id = Column('item_id', Integer, ForeignKey('items.id'))
    _shop_type_id = Column('shop_type_id', Integer, ForeignKey('shop_types.id'))
    cost = Column(Integer)

    item = relationship('Item', uselist=False)
    type = relationship('ShopType', uselist=False)

    def __repr__(self):
        return "<ShopItem(item='{}',cost='{}')>".format(
            self.item, self.cost
        )


# DONE
class EquipmentSlot(Base):
    """
    EquipmentSlot class

    Slots:
        Weapon
        Shield
    """

    __tablename__ = 'equipment_slots'

    _id = Column('id', Integer, primary_key=True)
    name = Column(Integer, unique=True)

    def __repr__(self):
        return "<EquipmentSlot(name='{}')>".format(self.name)


# DONE
class CharacterEquipment(Base):
    """CharacterEquipment class"""

    __tablename__ = 'character_equipments'

    _id = Column('id', Integer, primary_key=True)
    _character_id = Column('character_id', Integer, ForeignKey('characters.id'))
    _item_id = Column('item_id', Integer, ForeignKey('items.id'))
    _equipment_slot_id = Column('equipment_slot_id', Integer, ForeignKey('equipment_slots.id'))

    character = relationship('Character', back_populates='equipments', uselist=False)
    item = relationship('Item', uselist=False)
    equipment_slot = relationship('EquipmentSlot', uselist=False)

    def __repr__(self):
        return "<CharacterEquipment(item='{}', equipment_slot='{}')>".format(
            self.item, self.equipment_slot
        )


# DONE
class Location(Base):
    """Location class"""

    __tablename__ = 'locations'

    _id = Column('id', Integer, primary_key=True)
    name = Column(String(20), unique=True)
    description = Column(Text)

    characters = relationship('Character', secondary=character_location, back_populates='location')
    entities = relationship('Entity', secondary=entity_location, back_populates='location')

    def __repr__(self):
        return "<Location(name='{}', description='{}')>".format(self.name, self.description)


# DONE
class EntityType(Base):
    """
    EntityType class

    Types:
        Hostile
        Friendly
    """

    __tablename__ = 'entity_types'

    _id = Column('id', Integer, primary_key=True)
    name = Column(String(20), unique=True)

    entities = relationship('Entity', back_populates='entity_type')

    def __repr__(self):
        return "<EntityType(name='{}')>".format(self.name)


# DONE
class Entity(Base):
    """Entity class"""

    __tablename__ = 'entities'

    _id = Column('id', Integer, primary_key=True)
    _entity_type_id = Column('entity_type_id', Integer, ForeignKey('entity_types.id'))
    level = Column(Integer)
    _current_hp = Column('current_hp', Integer)
    name = Column(String(20), unique=True)
    description = Column(Text)

    entity_type = relationship('EntityType', back_populates='entities', uselist=False)
    attribute = relationship('Attribute', secondary=entity_attribute, uselist=False)
    location = relationship('Location', secondary=entity_location, back_populates='entities', uselist=False)
    entity_loot = relationship('EntityLoot', uselist=False)

    @hybrid_property
    def current_hp(self):
        return self._current_hp

    @current_hp.setter
    def current_hp(self, value):
        if self.max_hp:
            if value > self.max_hp:
                raise ValueError('Value exceeds the max_hp')
        self._current_hp = value

    @hybrid_property
    def max_hp(self):
        if self.attribute:
            return self.attribute.hp
        else:
            return None

    @max_hp.setter
    def max_hp(self, value):
        if not self.attribute:
            self.attribute = Attribute()
        self.attribute.hp = value

    @hybrid_property
    def strength(self):
        if self.attribute:
            return self.attribute.strength
        else:
            return None

    @strength.setter
    def strength(self, value):
        if not self.attribute:
            self.attribute = Attribute()
        self.attribute.strength = value

    @hybrid_property
    def defense(self):
        if self.attribute:
            return self.attribute.defense
        else:
            return None

    @defense.setter
    def defense(self, value):
        if not self.attribute:
            self.attribute = Attribute()
        self.attribute.defense = value

    def __repr__(self):
        return "<Entity(level='{}', name='{}', description='{}')>".format(
            self.level, self.name, self.description
        )


# DONE
class EntityLoot(Base):
    """EntityLoot class"""

    __tablename__ = 'entity_loots'

    _id = Column('id', Integer, primary_key=True)
    _entity_id = Column('entity_id', Integer, ForeignKey('entities.id'))
    exp = Column(Integer)
    money = Column(Integer)

    items = relationship('LootItem')

    def __repr__(self):
        return "<EntityLoot(exp='{}', money='{}')>".format(
            self.exp, self.money
        )


# DONE
class LootItem(Base):
    """LootItem class"""

    __tablename__ = 'loot_items'

    _entity_loot_id = Column('entity_loot_id', ForeignKey('entity_loots.id'), primary_key=True)
    _item_id = Column('item_id', ForeignKey('items.id'), primary_key=True)
    drop_chance = Column(Float)
    drop_amount_minimum = Column(Integer)
    drop_amount_maximum = Column(Integer)

    def __repr__(self):
        return "<EntityLootItem(drop_chance='{}', drop_amount_minimum='{}', drop_amount_maximum='{}')>".format(
            self.drop_chance, self.drop_amount_minimum, self.drop_amount_maximum
        )


# DONE
class CharacterCompanion(Base):
    """Companion class"""

    __tablename__ = 'character_companions'

    _character_id = Column('character_id', Integer, ForeignKey('characters.id'), primary_key=True)
    _entity_id = Column('entity_id', Integer, ForeignKey('entities.id'), primary_key=True)
    main = Column(Boolean)
    apply_attribute = Column(Boolean)
    action_duration = Column(Interval)
    action_started = Column(DateTime)

    entity = relationship('Entity', uselist=False)

    def __repr__(self):
        return "<CharacterCompanion(main='{}', apply_attribute='{}', action_duration='{}', action_started='')>".format(
            self.main, self.apply_attribute, self.action_duration, self.action_started
        )


# Done
item_plan_materials = Table(
    'item_plan_materials',
    Base.metadata,
    Column('item_plan_id', Integer, ForeignKey('item_plans.id'), primary_key=True),
    Column('plan_material_id', Integer, ForeignKey('plan_materials.id'), primary_key=True)
)


# Done
class PlanMaterial(Base):
    __tablename__ = 'plan_materials'

    _id = Column('id', Integer, primary_key=True)
    _item_id = Column('item_id', Integer, ForeignKey('items.id'))
    amount = Column(Integer)

    item = relationship('Item', uselist=False)


# Done
class ItemPlan(Base):
    __tablename__ = 'item_plans'

    _id = Column('id', Integer, primary_key=True)
    _item_id = Column('item_id', Integer, ForeignKey('items.id'))

    item = relationship('Item', uselist=False)
    materials = relationship('PlanMaterial', secondary=item_plan_materials)
