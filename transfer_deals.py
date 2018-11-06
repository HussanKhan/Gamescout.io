from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_create.database_generation import Games, MasterGames
from sqlalchemy.ext.declarative import declarative_base
from game_info.clean_title import clean_title as cleaner

# Creates handler
Base1 = declarative_base()

#  creates engine
engine1 = create_engine('sqlite:///gamedeals.db')

# Combines handler and engine
Base1.metadata.bind = engine1

# Creates a unique session
DBSession1 = sessionmaker(bind=engine1)

# Activating session
session1 = DBSession1()

# Creates handler
Base2 = declarative_base()

#  creates engine
engine2 = create_engine('sqlite:///master_gamelist.db')

# Combines handler and engine
Base2.metadata.bind = engine2

# Creates a unique session
DBSession2 = sessionmaker(bind=engine2)

# Activating session
session2 = DBSession2()

daily_deals = session1.query(Games).all()

for entry in daily_deals:
    gtitle = cleaner(entry.title)[0]
    try:
        session2.query(MasterGames).filter_by(title=gtitle).one()
    except Exception:
        print("Added {}".format(gtitle))
        attr = MasterGames(title=gtitle, genre=entry.genre, image=entry.image)
        session2.add(attr)
        session2.commit()
