import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.getenv('DB_URL'))

Session = sessionmaker(bind=engine)
session = Session()


def connect_engine():
    engine.connect()


def commit():
    session.commit()
