from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from url_map_pro import UrlMap

class UrlUpdate():

    def __init__(self):
        self.Base = declarative_base()
        self.engine = create_engine('postgresql://webdevkhan:Mrjubble@localhost:5432/webdevkhan')
        # Combines handler and engine
        self.Base.metadata.bind = self.engine
        # Creates a unique session
        self.DBSession = sessionmaker(bind=self.engine)
        # Activating session
        self.session = self.DBSession()

    def update_url(self, url):
        try:
            url = self.session.query(UrlMap).filter_by(url=url).one()
            vis = url.visits
            url.visits = vis + 1
            self.session.commit()
        except Exception:
            visit = 1
            adding = UrlMap(url=url, visits = visit)
            self.session.add(adding)
            self.session.commit()

    def close_session(self):
        self.session.close()
        return 1
