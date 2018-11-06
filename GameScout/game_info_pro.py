from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Stores deep game information
class DeepGame(Base):
    __tablename__ = 'DeepGame'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    release_date = Column(String)
    image = Column(String)
    genre = Column(String)
    rating = Column(String)
    summary = Column(String)
    storyline = Column(String)
    trailer = Column(String)

# Stores surface level information of current deals
class CurrentDeals(Base):
    __tablename__ = 'CurrentDeals'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    buy_link = Column(String)
    price = Column(String)
    platform = Column(String)
    deep_name = Column(String)

engine = create_engine('postgresql://webdevkhan:Mrjubble@localhost:5432/webdevkhan')
Base.metadata.create_all(engine)
