from datetime import datetime, timedelta

from sqlalchemy import Column, Table, Integer, String, Text, BigInteger, ForeignKey, DateTime, Interval
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import properties as prop
from utils import occurrence

Base = declarative_base()

# TODO: add entity loot item

""""

    Association tables
    
"""
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


# TODO: add companion, a friendly entity in the character
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
    # equipments = relationship('CharacterEquipment', back_populates='character')
    location = relationship('Location', secondary=character_location, back_populates='characters', uselist=False)

    def is_full_hp(self):
        return self.current_hp == self.max_hp

    def is_alive(self):
        return self.current_hp > 0

    @hybrid_property
    def current_hp(self):
        if self.max_hp:  # if max hp is not None
            if self._current_hp < self.max_hp:
                regen = occurrence(self._hp_last_updated, prop.GEN_HP_INTERVAL) * prop.GEN_HP_AMOUNT
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
    name = Column(String(20), unique=True)

    items = relationship('Item', back_populates='item_type')

    def __repr__(self):
        return "<ItemType(name='{}')>".format(self.name)


# DONE
class Item(Base):
    """Item class"""

    __tablename__ = 'items'

    _id = Column('id', Integer, primary_key=True)
    _item_type_id = Column('item_type_id', Integer, ForeignKey('item_types.id'))
    name = Column(String(20), unique=True)
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
        common
        exclusive
    """

    __tablename__ = 'shop_types'

    _id = Column('id', Integer, primary_key=True)
    name = Column(String(10), unique=True)

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


class EquipmentSlot(Base):
    """EquipmentSlot class"""

    __tablename__ = 'equipment_slots'

    id = Column(Integer, primary_key=True)
    name = Column(Integer, unique=True)

    def __repr__(self):
        return "<EquipmentSlot(id='{}', name='{}')>".format(self.id, self.name)


class CharacterEquipment(Base):
    """CharacterEquipment class"""

    __tablename__ = 'character_equipments'

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    equipment_slot_id = Column(Integer, ForeignKey('equipment_slots.id'))

    # character = relationship('Character', back_populates='equipments', uselist=False)
    item = relationship('Item', uselist=False)
    equipment_slot = relationship('EquipmentSlot', uselist=False)

    def __repr__(self):
        return "<CharacterEquipment(id='{}', character_id='{}', item_id='{}', equipment_slot_id='{}')>".format(
            self.id, self.character_id, self.item_id, self.equipment_slot_id
        )


class Location(Base):
    """Location class"""

    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(Integer, unique=True)
    description = Column(Text)

    characters = relationship('Character', secondary=character_location, back_populates='location')
    entities = relationship('Entity', secondary=entity_location, back_populates='location')

    def __repr__(self):
        return "<Location(id='{}', name='{}', description='{}')>".format(self.id, self.name, self.description)


class EntityType(Base):
    """EntityType class"""

    __tablename__ = 'entity_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)

    entities = relationship('Entity', back_populates='entity_type')

    def __repr__(self):
        return "<EntityType(id='{}', name='{}')>".format(self.id, self.name)


class Entity(Base):
    """Entity class"""

    __tablename__ = 'entities'

    id = Column(Integer, primary_key=True)
    entity_type_id = Column(Integer, ForeignKey('entity_types.id'))
    name = Column(String(20), unique=True)
    description = Column(Text)
    level = Column(Integer)
    hp = Column(Integer)

    entity_type = relationship('EntityType', back_populates='entities', uselist=False)
    location = relationship('Location', secondary=entity_location, back_populates='entities', uselist=False)
    attribute = relationship('Attribute', secondary=entity_attribute, uselist=False)

    def __repr__(self):
        return "<Entity(id='{}', entity_type_id='{}', name='{}', description='{}', level='{}')>".format(
            self.id, self.entity_type_id, self.name, self.description, self.level
        )


class LootItem:
    # TODO: add loot item

    """LootItem class"""

    __tablename__ = 'loot_items'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))


class EntityLoot:
    # TODO: add entity loot
    pass
