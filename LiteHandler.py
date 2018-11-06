from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_create.database_generation import Games, CommonNames
from sqlalchemy.ext.declarative import declarative_base

class LiteQueryC():
    """This class is used to handle two sqlite databases"""

    def __init__(self):
        self.Base = declarative_base()
        self.engine = create_engine('sqlite:///commonnames.db')
        self.Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def query_name(self, name):
        try:
            n_search = self.session.query(CommonNames).filter_by(commone_name = name).all()
            return n_search[0]
        except Exception:
            return "NONE"

    def query_all(self):
        search = self.session.query(CommonNames).all()
        return search

    def append_entry(self, c_name, d_name):
        entry = CommonNames(commone_name = c_name, deep_name = d_name)
        self.session.add(entry)
        self.session.commit()


class LiteQueryG():
    """This class is used to handle two sqlite databases"""

    def __init__(self):
        self.Base = declarative_base()
        self.engine = create_engine('sqlite:///gamedeals.db')
        self.Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def query_name(self, name):
        try:
            n_search = self.session.query(Games).filter_by(commone_name = name).one()
            return n_search
        except Exception:
            return "NONE"

    def query_all(self):
        search = self.session.query(Games).distinct(Games.buy_link).group_by(Games.buy_link)
        return search

    def commit_game(self):
        self.session.commit()

    def gen_match(self, gen):
        result = self.session.query(Games).filter(Games.genre.like("%" + gen + "%")).all()
        return result

    def delete_all(self):
        game_stuff = self.session.query(Games).delete()
        self.session.commit()
