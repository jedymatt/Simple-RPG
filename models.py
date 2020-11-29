from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Table, Integer, String, Text, BigInteger, ForeignKey, TIMESTAMP, Interval
from sqlalchemy.orm import relationship

Base = declarative_base()

# TODO: add entity loot item

"""
------------------------------------------------------------------------------------------------------------------------
    Associative Tables will always be placed above the topmost class
"""

character_attribute = Table(
    'character_attributes',
    Base.metadata,
    Column('character_id', ForeignKey('characters.id')),
    Column('attribute_id', ForeignKey('attributes.id'))
)

character_location = Table(
    'character_locations',
    Base.metadata,
    Column('character_id', ForeignKey('characters.id')),
    Column('location_id', ForeignKey('locations.id'))
)

item_attribute = Table(
    'item_attributes',
    Base.metadata,
    Column('item_id', ForeignKey('items.id')),
    Column('attribute_id', ForeignKey('attributes.id'))
)

entity_attribute = Table(
    'entity_attributes',
    Base.metadata,
    Column('entity_id', ForeignKey('entities.id')),
    Column('attribute_id', ForeignKey('attributes.id'))
)

entity_location = Table(
    'entity_locations',
    Base.metadata,
    Column('entity_id', ForeignKey('entities.id')),
    Column('location_id', ForeignKey('locations.id'))
)

"""
------------------------------------------------------------------------------------------------------------------------
"""


class User(Base):
    """User class"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger, unique=True)
    init_roll = Column(Integer)

    character = relationship('Character', back_populates='user', uselist=False)

    def __repr__(self):
        return "<User(id='{}', discord_id='{}' init_roll='{}')>".format(self.id, self.discord_id, self.init_roll)


class Attribute(Base):
    """Attribute class"""

    __tablename__ = 'attributes'

    id = Column(Integer, primary_key=True)
    hp = Column(Integer)
    strength = Column(Integer)
    defense = Column(Integer)

    def __repr__(self):
        return "<Attribute(id='{}', current_hp='{}', strength='{}', defense='{}')>".format(
            self.id, self.hp, self.strength, self.defense
        )


class Character(Base):
    """Character class"""

    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    level = Column(Integer)
    exp = Column(Integer)
    current_hp = Column(Integer)  # current current_hp
    money = Column(Integer)

    attribute = relationship('Attribute', secondary=character_attribute, uselist=False)
    user = relationship('User', back_populates='character', uselist=False)
    items = relationship('CharacterItem', back_populates='character')
    equipments = relationship('CharacterEquipment', back_populates='character')
    location = relationship('Location', secondary=character_location, back_populates='characters', uselist=False)

    def __repr__(self):
        return "<Character(id='{}', user_id='{}', level='{}', exp='{}', money='{}')>".format(
            self.id, self.user_id, self.level, self.exp, self.money
        )


class ItemType(Base):
    """ItemType class"""

    __tablename__ = 'item_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)

    items = relationship('Item', back_populates='item_type')

    def __repr__(self):
        return "<ItemType(id='{}', name='{}')>".format(self.id, self.name)


class EffectAttribute(Base):
    """EffectAttribute class"""
    __tablename__ = 'effect_attributes'

    id = Column(Integer, primary_key=True)
    attribute_id = Column(Integer, ForeignKey('attributes.id'))
    duration = Column(Interval)


class Item(Base):
    """Item class"""

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    item_type_id = Column(Integer, ForeignKey('item_types.id'))
    name = Column(String(20), unique=True)
    description = Column(Text)

    item_type = relationship('ItemType', back_populates='items', uselist=False)
    attribute = relationship('Attribute', secondary=item_attribute, uselist=False)

    # effect = relationship

    def __repr__(self):
        return "<Item(id='{}', item_type_id='{}', name='{}', description='{}')>".format(
            self.id, self.item_type_id, self.name, self.description
        )


class ShopItem(Base):
    """ShopItem class"""

    __tablename__ = 'shop_items'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    cost = Column(Integer)
    item = relationship('Item', uselist=False)

    def __repr__(self):
        return "<ShopItem(id='{}', item_id='{}', cost='{}')>".format(
            self.id, self.item_id, self.cost
        )


class CharacterItem(Base):
    """CharacterItem class"""

    __tablename__ = 'character_items'

    # id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    amount = Column(Integer)

    character = relationship('Character', back_populates='items', uselist=False)
    item = relationship('Item')

    def __repr__(self):
        return "<CharacterItem(character_id='{}', item_id='{}')>".format(
            self.character_id, self.item_id
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

    character = relationship('Character', back_populates='equipments', uselist=False)
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
