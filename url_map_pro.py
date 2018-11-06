from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Stores deep game information
class UrlMap(Base):
    __tablename__ = 'UrlMap'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    visits = Column(Integer)

engine = create_engine('postgresql://webdevkhan:Mrjubble@localhost:5432/webdevkhan')
Base.metadata.create_all(engine)
