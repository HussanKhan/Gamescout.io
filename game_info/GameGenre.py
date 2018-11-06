def get_details(game_name):
    from igdb_api_python.igdb import igdb
    import datetime
    now = datetime.datetime.now()

    igdb = igdb("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

    try:
        #Search on games endpoint
        result = igdb.games({
            'search': game_name,
            'fields' : ['genres', 'themes', 'name', 'cover', 'release_dates', 'aggregated_rating', 'summary', 'videos', 'storyline']
        })

        # Finds most common genres code for similar games
        all_genres_ids = []

        # Finds most common theme code for similar games
        all_themes_ids = []

        # Extracts trailer link
        game = result.body[0]

        try:
            vid = game.get('videos')[0]["video_id"]
        except Exception:
            vid = "NONE"

        # Extracts game summary
        try:
            story = game.get('summary')
        except Exception:
            store = "No Summary Available"

        try:
            line = game.get('storyline')
        except Exception:
            line = "No Story Available"

        # Release Date
        try:
            rd = game.get('release_dates')[0]['human']
            release_date = game.get('release_dates')[0]['human']
            rd = int(rd[:4]) # extracts year
            if (int(now.year) - rd) == 0:
                rd = "Recently Released Games"
            elif (int(now.year) - rd) == 1:
                rd = "Released Last Year"
            else:
                rd = "OLDER"
        except Exception:
            release_date = "Unknown"
            rd = "NONE"

        # Creating image url
        try:
            cover_image_url = game.get('cover')
            cover_image_url = 'https:'+ cover_image_url['url'].replace('t_thumb', 't_cover_big')
        except Exception:
            cover_image_url = "NONE"

        # Extracts rating
        try:
            rating = game.get('aggregated_rating')
        except Exception:
            rating = "----"

        # Extracts rating
        try:
            name = game.get('name')
        except Exception:
            name = "NONE"

        # Fill genre and themes array
        if game.get("genres"):
            genres = game.get('genres')
            for n in genres:
                all_genres_ids.append(int(n))

        if game.get('themes'):
            theme = game.get("themes")
            for n in theme:
                all_themes_ids.append(int(n))

        # Holds relevant and unique genres
        genres_ids = []

        # Holds relevant and unique themes
        themes_ids = []

        # just to catch outlier genres like pinball
        for id in all_genres_ids:
            if id not in genres_ids:
                genres_ids.append(id)

        # just to catch outlier genres like pinball
        for theme in all_themes_ids:
            if theme not in themes_ids:
                themes_ids.append(theme)

        # Genres ID to genres name mappings
        genres = {
        2: "Point-and-click",
        4: "Fighting Games",
        5: "Shooter Games",
        7: "Music Games",
        8: "Platform Games",
        9: "Puzzle Games",
        10: "Racing Games",
        11: "Real Time Strategy (RTS) Games",
        12: "Role-playing (RPG) Games",
        13: "Simulator Games",
        14: "Sport Games",
        15: "Strategy Games",
        16: "Turn-based strategy (TBS) Games",
        24: "Tactical Games",
        25: "Hack and slash/Beat 'em up Games",
        26: "Quiz/Trivia Games",
        30: "Pinball Games",
        31: "Adventure Games",
        32: "Indie Games",
        33: "Aracde"}

        # Themes ID to theme name mappings
        themes = {
        1: "Action Games",
        17: "Fantasy Games",
        18: "Science Fiction Games",
        19: "Horror Games",
        20: "Thriller Games",
        21: "Survival Games",
        22: "Historical Games",
        23: "Stealth Games",
        27: "Comedy Games",
        28: "Business Games",
        31: "Drama Games",
        32: "Non-fiction Games",
        33: "Sandbox Games",
        34: "Educational Games",
        35: "Kids Games",
        38: "Open World Games",
        39: "Warfare Games",
        40: "Party Games",
        41: "Explore, Expand, Exploit, and Exterminate Games",
        42: "Erotic Games",
        43: "Mystery Games"
        }

        related_words = []

        for t_id in themes_ids:
            try:
                related_words.append(themes[int(t_id)])
            except Exception:
                pass

        for g_id in genres_ids:
            try:
                related_words.append(genres[int(g_id)])
            except Exception:
                pass

        # Appends release date to genres for later sorting
        related_words.append(rd)

        try:
            # If rating is high enough, appends list
            if int(str(rating)[:2]) > 87:
                related_words.append("Highly Rated Games")
        except Exception:
            pass

        return {"name": name, "genre": related_words, "image": cover_image_url, "rating": str(rating)[:2], "summary": story, "trailer": vid, "release_date": release_date, "storyline": line}
    except Exception:
        return "NONE"
