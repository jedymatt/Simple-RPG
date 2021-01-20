from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Attribute(Base):
    __tablename__ = 'attributes'

    id = Column(Integer, primary_key=True)
    hp = Column(Float, default=0)
    strength = Column(Float, default=0)
    defense = Column(Float, default=0)

    def __repr__(self):
        return "<Attribute(hp='%s', strength='%s', defense='%s')>" % (self.hp, self.strength, self.defense)

    @classmethod
    def copy(cls, other):
        return Attribute(hp=other.hp, strength=other.strength, defense=other.defense)


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(Text)
    unlock_level = Column(Integer, default=0)

    materials: list = relationship('RawMaterial', back_populates='location')

    def __repr__(self):
        return "<Location(name='%s', unlock_level='%s')>" % (self.name, self.unlock_level)
