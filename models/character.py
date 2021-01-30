from models.base import Attribute, Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship
from models.util import occurrence
from models.config import HP_REGEN_AMOUNT, HP_REGEN_INTERVAL, BASE_HP, BASE_DEFENSE, BASE_STRENGTH
from datetime import datetime
from math import floor
from sqlalchemy.ext.hybrid import hybrid_property


class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    stat_growth = Column(Float)
    _current_hp = Column('current_hp', Integer)
    type = Column(String(50))
    attribute_id = Column(ForeignKey('attributes.id'))
    location_id = Column(ForeignKey('locations.id'))

    attribute = relationship('Attribute', foreign_keys=[attribute_id], uselist=False)
    location = relationship('Location', foreign_keys=[location_id], uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'character',
        'polymorphic_on': type
    }

    @hybrid_property
    def current_hp(self):
        return self._current_hp

    @current_hp.setter
    def current_hp(self, value):
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
        return "<Character(level='%s', exp='%s', current_hp='%s' type='%s')>" % (
            self.level,
            self.exp,
            self._current_hp,
            self.type
        )


class PlayerItem(Base):
    __tablename__ = 'player_items'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('characters.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    amount = Column(Integer)

    item = relationship('Item', uselist=False)

    @hybrid_property
    def name(self):
        if self.item:
            return self.item.name
        return None


class Player(Character):
    user_id = Column(Integer, ForeignKey('users.id'))
    money = Column(Integer, default=0)
    hp_last_updated = Column(DateTime(timezone=True), default=func.now())
    companion_id = Column(Integer, ForeignKey('characters.id'))

    user = relationship('User', back_populates='player', uselist=False)
    items: list = relationship('PlayerItem')
    equipment = relationship('EquipmentSet', uselist=False)
    companion = relationship('Friendly', foreign_keys=[companion_id], uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'player',
        'polymorphic_load': 'selectin'
    }

    def is_full_hp(self):
        return self.current_hp == self.max_hp

    @hybrid_property
    def current_hp(self):
        if self._current_hp and self.max_hp:  # if max hp is not None

            if self._current_hp < self.max_hp:

                regen = occurrence(self.hp_last_updated, HP_REGEN_INTERVAL) * HP_REGEN_AMOUNT
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
                    self.hp_last_updated = datetime.now()

        self._current_hp = value

    def next_level_exp(self):
        base_exp = 200
        return floor(base_exp * (self.level ** 1.2))

    def level_up(self):

        # get stat to be added by getting the differences
        gap_str = floor(BASE_STRENGTH * (self.stat_growth ** (self.level + 1))) - floor(
            BASE_STRENGTH * (self.stat_growth ** self.level))
        gap_def = floor(BASE_DEFENSE * (self.stat_growth ** (self.level + 1))) - floor(
            BASE_DEFENSE * (self.stat_growth ** self.level))

        self.strength += gap_str
        self.defense += gap_def

        self.level += 1

    def add_exp(self, value):
        if value < 0:
            raise ValueError('value is lesser or equal zero')

        self.exp += value
        if self.exp >= self.next_level_exp():
            self.exp -= self.next_level_exp()
            self.level_up()


class EquipmentSet(Base):
    __tablename__ = 'equipment_sets'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('characters.id'))
    weapon_id = Column(Integer, ForeignKey('items.id'))
    shield_id = Column(Integer, ForeignKey('items.id'))

    weapon = relationship('Weapon', uselist=False, foreign_keys=[weapon_id])
    shield = relationship('Shield', uselist=False, foreign_keys=[shield_id])


class Entity(Character):
    name = Column(String(50))
    base_id = Column(Integer, ForeignKey('attributes.id'))

    base = relationship('Attribute', foreign_keys=[base_id], uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'entity',
        'polymorphic_load': 'selectin'
    }

    def set_level(self, value):
        self.restore()
        base_hp = self.base.hp
        base_str = self.base.strength
        base_def = self.base.defense
        self.max_hp = floor(base_hp * (self.stat_growth ** value))
        self.current_hp = self.max_hp
        self.strength = floor(base_str * (self.stat_growth ** value))
        self.defense = floor(base_def * (self.stat_growth ** value))

        self.level = value

    def restore(self):
        self.max_hp = self.base.hp
        self.current_hp = self.max_hp
        self.strength = self.base.strength
        self.defense = self.base.defense


class Friendly(Entity):
    __mapper_args__ = {
        'polymorphic_identity': 'friendly',
        'polymorphic_load': 'inline'
    }


class Hostile(Entity):
    # add loot reward
    loot_id = Column(Integer, ForeignKey('loots.id'))
    loot = relationship('Loot', uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'hostile',
        'polymorphic_load': 'inline'
    }
