from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Stores deep game information
class VidRev(Base):
    __tablename__ = 'VidRev'
    id = Column(Integer, primary_key=True)
    deep_name = Column(String)
    review_link = Column(Integer)

engine = create_engine('postgresql://webdevkhan:Mrjubble@localhost:5432/webdevkhan')
Base.metadata.create_all(engine)
