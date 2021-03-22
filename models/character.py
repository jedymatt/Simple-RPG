from datetime import datetime, timezone
from math import floor

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Float
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from models.base import Attribute, Base
from models.config import HP_REGEN_AMOUNT, HP_REGEN_INTERVAL, BASE_DEFENSE, BASE_STRENGTH
from models.util import occurrence


class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    stat_growth = Column(Float)
    type = Column(String(50))
    attribute_id = Column(ForeignKey('attributes.id'))
    location_id = Column(ForeignKey('locations.id'))

    attribute = relationship('Attribute', foreign_keys=[attribute_id], uselist=False)
    location = relationship('Location', foreign_keys=[location_id], uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'character',
        'polymorphic_on': type
    }

    # TODO: Formulate taking damage
    def take_damage(self, hit_points):
        pass

    @hybrid_property
    def current_hp(self):
        if self.attribute:
            return self.attribute.current_hp
        else:
            return None

    @current_hp.setter
    def current_hp(self, value):
        if not self.attribute:
            self.attribute = Attribute()
        self.attribute.current_hp = value

    @hybrid_property
    def max_hp(self):
        if self.attribute:
            return self.attribute.max_hp
        else:
            return None

    @max_hp.setter
    def max_hp(self, value):
        if not self.attribute:
            self.attribute = Attribute()
        self.attribute.max_hp = value

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
        return "<Character(level='%s', exp='%s', type='%s')>" % (
            self.level,
            self.exp,
            self.type
        )


class PlayerItem(Base):
    __tablename__ = 'player_items'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('characters.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    amount = Column(Integer)

    item = relationship('Item', uselist=False)


class Player(Character):
    user_id = Column(Integer, ForeignKey('users.id'))
    money = Column(Integer, default=0)
    hp_last_updated = Column(DateTime(timezone=True), default=func.now())
    companion_id = Column(Integer, ForeignKey('characters.id'))

    user = relationship('User', back_populates='player', uselist=False)
    items: list = relationship('PlayerItem')
    equipment_set = relationship('EquipmentSet', uselist=False)
    companion = relationship('Friendly', foreign_keys=[companion_id], uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'player',
        'polymorphic_load': 'selectin'
    }

    def is_full_hp(self):
        return self.current_hp == self.max_hp

    @hybrid_property
    def current_hp(self):
        if self.attribute.current_hp and self.max_hp:  # if max hp is not None

            if self.attribute.current_hp < self.max_hp:

                regen = occurrence(self.hp_last_updated, HP_REGEN_INTERVAL) * HP_REGEN_AMOUNT
                self.attribute.current_hp += regen

                if self.attribute.current_hp > self.max_hp:  # if current hp exceeds the max hp
                    self.attribute.current_hp = self.max_hp  # set the current hp value as max hp

        return self.attribute.current_hp

    @current_hp.setter
    def current_hp(self, value):
        if self.max_hp:  # if max hp is not None
            if value > self.max_hp:
                raise ValueError('Value exceeds the max_hp')

            if self.is_full_hp():  # condition first if value is full hp
                self.hp_last_updated = datetime.now(tz=timezone.utc)

        self.attribute.current_hp = value

    @hybrid_property
    def max_hp(self):
        return self.attribute.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.attribute.max_hp = value
        self.hp_last_updated = datetime.now(tz=timezone.utc)

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

    def __repr__(self):
        return "EquipmentSet(weapon='%s', shield='%s')" % (self.weapon.name, self.shield.name)


class Entity(Character):
    name = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'entity',
        'polymorphic_load': 'selectin'
    }


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
