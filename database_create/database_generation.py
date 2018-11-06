import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base1 = declarative_base()
Base2 = declarative_base()

class Games(Base1):
    __tablename__ = 'game_deals'

    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String, nullable=False)
    price = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    image = Column(String, nullable=False)
    source = Column(String, nullable=False)
    buy_link = Column(String, nullable=False)

engine1 = create_engine('sqlite:///gamedeals.db')
Base1.metadata.create_all(engine1)

class CommonNames(Base2):
    __tablename__ = 'CommonNames'

    id = Column(Integer, primary_key=True, unique=True)
    commone_name = Column(String)
    deep_name = Column(String)

engine2 = create_engine('sqlite:///commonnames.db')
Base2.metadata.create_all(engine2)
