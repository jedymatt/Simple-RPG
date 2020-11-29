import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(os.getenv('DB_URL'))

Session = sessionmaker(bind=engine)
session = Session()


def connect_engine():
    engine.connect()
