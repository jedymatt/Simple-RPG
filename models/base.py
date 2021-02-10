from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Attribute(Base):
    __tablename__ = 'attributes'

    id = Column(Integer, primary_key=True)
    current_hp = Column(Float, default=0)
    max_hp = Column(Float, default=0)
    strength = Column(Float, default=0)
    defense = Column(Float, default=0)

    @property
    def attrs(self):
        return ['max_hp', 'strength', 'defense']

    def __repr__(self):
        return "<Attribute(current_hp='%s', max_hp='%s', strength='%s', defense='%s')>" % (
            self.current_hp, self.max_hp, self.strength, self.defense
        )

    def __add__(self, other):

        if float(other.current_hp).is_integer():
            self.current_hp += other.current_hp
            if self.current_hp >= self.max_hp:
                self.current_hp = self.max_hp
        else:
            self.current_hp += round(self.max_hp * other.current_hp)
            if self.current_hp >= self.max_hp:
                self.current_hp = self.max_hp

        if float(other.max_hp).is_integer():
            self.max_hp += other.max_hp
        else:
            self.max_hp += round(self.max_hp * other.max_hp)

        if float(other.strength).is_integer():
            self.strength += other.strength
        else:
            self.strength += round(self.strength * other.strength)

        if float(other.defense).is_integer():
            self.defense += other.defense
        else:
            self.defense += round(self.defense * other.defense)
        return self

    def __sub__(self, other):
        self.max_hp -= other.max_hp
        self.strength -= other.strength
        self.defense -= other.defense

        return self


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(Text)
    unlock_level = Column(Integer, default=0)

    raw_materials: list = relationship('LocationRawMaterial', back_populates='location')

    def __repr__(self):
        return "<Location(name='%s', unlock_level='%s')>" % (self.name, self.unlock_level)


class LocationRawMaterial(Base):
    __tablename__ = 'location_raw_materials'

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    raw_material_id = Column(Integer, ForeignKey('items.id'))
    drop_chance = Column(Float)
    drop_amount_min = Column(Integer)
    drop_amount_max = Column(Integer)

    location = relationship('Location', back_populates='raw_materials', foreign_keys=[location_id], uselist=False)
    raw_material = relationship('RawMaterial', back_populates='location', foreign_keys=[raw_material_id], uselist=False)
