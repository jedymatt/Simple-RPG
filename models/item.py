from models.base import Base
from sqlalchemy import Column, Integer, String, Interval, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import timedelta


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(Text)
    type = Column(String(50))
    market_value = Column(Integer, default=0)

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type
    }

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "<Item(name='%s', type='%s')>" % (self.name, self.type)


class Consumable(Item):
    is_random_attr = Column(Boolean, default=True)
    attribute = relationship('Attribute', uselist=False)

    @declared_attr
    def attribute_id(cls):
        return Item.__table__.c.get('attribute_id', Column(ForeignKey('attributes.id')))

    __mapper_args__ = {
        'polymorphic_identity': 'consumable',
        'polymorphic_load': 'selectin'
    }


class RawMaterial(Item):
    # added location, TENTATIVE
    location = relationship('LocationRawMaterial', back_populates='raw_material', uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'raw_material',
        'polymorphic_load': 'selectin'
    }


class Equipment(Item):
    attribute = relationship('Attribute', uselist=False)

    @declared_attr
    def attribute_id(cls):
        return Item.__table__.c.get('attribute_id', Column(ForeignKey('attributes.id')))

    __mapper_args__ = {
        'polymorphic_identity': 'equipment',
        'polymorphic_load': 'selectin'
    }


class Weapon(Equipment):
    __mapper_args__ = {
        'polymorphic_identity': 'weapon',
        'polymorphic_load': 'inline'
    }


class Shield(Equipment):
    __mapper_args__ = {
        'polymorphic_identity': 'shield',
        'polymorphic_load': 'inline'
    }


class PlanMaterial(Base):
    __tablename__ = 'plan_materials'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    item_plan_id = Column(Integer, ForeignKey('item_plans.id'))
    amount = Column(Integer)

    item = relationship('Item', uselist=False)


class ItemPlan(Base):
    __tablename__ = 'item_plans'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))

    item = relationship('Item', uselist=False)
    materials: list = relationship('PlanMaterial')

    @hybrid_property
    def name(self):
        if self.item:
            return self.item.name
        return None


class ShopItem(Base):
    __tablename__ = 'shop_items'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))

    item = relationship('Item', uselist=False)
