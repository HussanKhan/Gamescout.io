import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base1 = declarative_base()

class Seed_Reviews(Base1):
    __tablename__ = 'Seed_Reviews'

    id = Column(Integer, primary_key=True, unique=True)
    game_name = Column(String, nullable=False)
    reviews = Column(String, nullable=False)

engine1 = create_engine('sqlite:///rev_seed.db')
Base1.metadata.create_all(engine1)
