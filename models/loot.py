from models.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship


class Loot(Base):
    __tablename__ = 'loots'

    id = Column(Integer, primary_key=True)
    exp = Column(Integer, default=0)
    money = Column(Integer, default=0)

    items: list = relationship('LootItem')


class LootItem(Base):
    __tablename__ = 'loot_items'

    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    loot_id = Column(Integer, ForeignKey('loots.id'), primary_key=True)
    drop_chance = Column(Float)
    drop_amount_min = Column(Integer)
    drop_amount_max = Column(Integer)

    item = relationship('Item', uselist=False)
