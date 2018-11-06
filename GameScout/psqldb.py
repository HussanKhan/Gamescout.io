from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from game_info_pro import DeepGame
from game_info.clean_title import clean_title as cleaner
from site_scrapers.YoutubeReview import YoutubeSearch
from stringtolist import stolist
from site_scrapers.ReviewScrape import Review

class GetGameInfo():

    def __init__(self):
        self.Base = declarative_base()
        self.engine = create_engine('postgresql://webdevkhan:Mrjubble@localhost:5432/webdevkhan')
        # Combines handler and engine
        self.Base.metadata.bind = self.engine
        # Creates a unique session
        self.DBSession = sessionmaker(bind=self.engine)
        # Activating session
        self.session = self.DBSession()
        self.rev = Review()
        self.brows = YoutubeSearch()

    def add_game_db(self, name, release_date, image, genre, rating, summary, storyline):
        # Before adding see if in db
        test_occ = self.session.query(DeepGame).filter_by(name = name).all()

        found = len(test_occ)

        if found == 0:
            # adds review to game b searching  youtube
            trail = self.brows.search(name + " game review")

            rev = self.rev.search(name)

            if rev:
                rev = str(rev)
            else:
                rev = "test"

            print("New Entry to DeepGame {}".format(name))

            # Game not in db add it

            adding = DeepGame(name = name, release_date = release_date, image = image, genre = genre,
            rating = rating, summary = summary, storyline = rev, trailer = trail)

            self.session.add(adding)
            self.session.commit()
        elif found == 1:
            try:
                # adding reviews to all games
                if "metacritic" not in test_occ[0].storyline and test_occ[0].storyline != "":

                    rev = self.rev.search(test_occ[0].name)

                    if rev:
                        rev = str(rev)
                    else:
                        rev = "metacritic_tried"

                    test_occ[0].storyline = rev
                    self.session.commit()
                    print("REVIEW ADDED")
                else:
                    print("REVIEW ALREADY IN DB")

                print("In DeepGame Already")
            except Exception:
                pass

    def dupe_remover(self, name):
        # Before adding see if in db
        test_occ = self.session.query(DeepGame).filter_by(name = name).all()

        found = len(test_occ)

        if found > 1:
            samp = test_occ[0]
            n = samp.name
            r = samp.release_date
            i = samp.image
            g = samp.genre
            rat = samp.rating
            s = samp.summary
            sto = samp.storyline
            tra = samp.trailer

            self.session.query(DeepGame).filter_by(name = name).delete()
            self.session.commit()

            # Readding result
            adding = DeepGame(name = n, release_date = r, image = i, genre = g,
            rating = rat, summary = s, storyline = sto, trailer = tra)

            self.session.add(adding)
            self.session.commit()



    def game_info(self, name):
        try:
            game_box = self.session.query(DeepGame).filter_by(name = name).all()
            return game_box[0]
        except Exception:
            return "NONE"

    def game_info_image(self, url):
        try:
            game_box = self.session.query(DeepGame).filter_by(image = url).all()
            return game_box[0]
        except Exception:
            return "NONE"

    def review_remap(self):
        test_occ = self.session.query(DeepGame).all()

        for g in test_occ:
            if g.image != "None" and "youtube" not in g.trailer:
                trail = self.brows.search(g.name + " game review")
                g.trailer = trail
                print("{} {}".format(g.name, trail))
                self.session.commit()

    def text_review(self, game_name, review):
        if game_name:
            game1 = self.session.query(DeepGame).filter_by(name = game_name).one()
            game1.storyline = review
            self.session.commit()
            print("ADDED REVIEW: {}".format(game_name))
        # if len(stolist(review)) > 2:
        #     game1 = self.session.query(DeepGame).filter_by(name = game_name).one()
        #     game1.storyline = review
        #     self.session.commit()
        # else:
        #     game1 = self.session.query(DeepGame).filter_by(name = game_name).one()
        #     game1.storyline = ""
        #     self.session.commit()

    def close_session(self):
        self.session.close()
        return 1

    def all_sess_close(self):
        self.engine.dispose()
