from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from game_info_pro import CurrentDeals
import json
from psqldb import GetGameInfo
from QualityCheck import qualitycontrol

Base = declarative_base()
engine = create_engine('postgresql://webdevkhan:Mrjubble@localhost:5432/webdevkhan')
# Combines handler and engine
Base.metadata.bind = engine
# Creates a unique session
DBSession = sessionmaker(bind=engine)
# Activating session
session = DBSession()

game_box = session.query(CurrentDeals).distinct(CurrentDeals.deep_name)

all_names = []

for n in game_box:
    all_names.append(n.deep_name)

with open("AllNames2018_2.json", "w") as newfile:
    json.dump({"names":all_names}, newfile)
    newfile.close()
