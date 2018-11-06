from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from game_info_pro import CurrentDeals
from game_info.clean_title import clean_title as cleaner

class GetDeals():

    def __init__(self):
        self.Base = declarative_base()
        self.engine = create_engine('postgresql://webdevkhan:Mrjubble@localhost:5432/webdevkhan')
        # Combines handler and engine
        self.Base.metadata.bind = self.engine
        # Creates a unique session
        self.DBSession = sessionmaker(bind=self.engine)
        # Activating session
        self.session = self.DBSession()

    def add_deal_db(self, title, buy_link, price, platform, deep_name):
        adding = CurrentDeals(title = title, buy_link = buy_link, price = price, platform = platform, deep_name = deep_name)
        self.session.add(adding)
        self.session.commit()

    def all_deals(self):
        game_box = self.session.query(CurrentDeals).all()
        return game_box

    def deal_info(self, title):
        game_box = self.session.query(CurrentDeals).filter_by(deep_name=title).all()
        return game_box

    def search_deal(self, name):
        game_box = self.session.query(CurrentDeals).filter_by(title=name).all()
        return game_box[0]

    def delete_deals(self):
        game_box = self.session.query(CurrentDeals).delete()
        self.session.commit()
        return "Done"

    def gen_match(self, gen):
        result = self.session.query(CurrentDeals).filter(CurrentDeals.genre.like("%" + gen + "%")).all()
        return result

    def uniqueurls(self):
        game_box = self.session.query(CurrentDeals).distinct(CurrentDeals.deep_name)
        urls = []
        for n in game_box:
            if n.deep_name:
                urls.append("https://gamescout.io/info/" + n.deep_name)

        return urls

    def close_session(self):
        self.session.close()
        return 1

    def all_sess_close(self):
        self.engine.dispose()
