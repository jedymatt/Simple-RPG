from models.base import Base
from sqlalchemy import Column, Integer, BigInteger, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import FetchedValue


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger, unique=True, nullable=False)
    dice_roll = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_online = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    player = relationship('Player', back_populates='user', uselist=False)

    def __repr__(self):
        return "<User(discord_id='%s', dice_roll='%s', last_online='%s')>" % (
            self.discord_id,
            self.dice_roll,
            self.last_online
        )
