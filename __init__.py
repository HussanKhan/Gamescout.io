#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/VgApp/vgdeals_production/")
import gzip
from flask import Flask, jsonify, make_response, request, render_template, redirect
from flask_cors import CORS
import os
import json
from pathlib2 import Path
from psqldb import GetGameInfo
import urllib.parse
from dealsdb import GetDeals
from urldb import UrlUpdate
from random import randint
import datetime
from QualityCheck import qualitycontrol
from stringtolist import stolist
from flask_gzip import Gzip
import content_gen



# formats source for deal
def find_source(link):
    if "gamestop" in link:
        return "GameStop"
    elif "razer" in link:
        return "Razer Gamestore"
    elif "humblebundle" in link:
        return "Humble Bundle"
    elif "amazon" in link:
        return "Amazon"
    elif "bestbuy" in link:
        return "Best Buy"
    elif "cdkeys" in link:
        return "CD Keys"


app = Flask(__name__)
gzip = Gzip(app)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')

# More Game Info
@app.route('/info/<title>', methods=["GET"])
def gameBox(title):
    deals_DATABASE = GetDeals()
    gamextra = GetGameInfo()
    # Finds game details from deep database
    db_res = gamextra.game_info(title)
    gamextra.close_session()

    try:
        # Finds deal related to game in current db
        game_deals = deals_DATABASE.deal_info(title)
    except Exception:
        game_deals = []

    deals_DATABASE.close_session()

    # creates url to game
    url = "https://gamescout.io/info/" + title

    # updates url
    url_db = UrlUpdate()
    url_db.update_url(url)

    url_db.close_session()

    # stores dict of all deals
    rel_deals = []

    today_deals = []

    price = False

    try:
        summary = db_res.summary
        if len(summary) > 500:
            summary = summary[:500]
    except Exception:
        summary = "None"

    try:
        rat = (int(db_res.rating)/20)
    except Exception:
        rat = 3

    rat_count = randint(3, 30)

    for d in game_deals:
        try:
            d_dict = {}
            d_dict["offer_title"] = d.title
            d_dict["platform"] = d.platform
            d_dict["buylink"] = d.buy_link
            d_dict["offer_phrase"] = d.price + " from " + find_source(d.buy_link)
            rel_deals.append(d_dict)
        except Exception:
            d_dict = {}
            d_dict["offer_title"] = d.title
            d_dict["platform"] = "PC"
            d_dict["buylink"] = d.buy_link
            d_dict["offer_phrase"] = d.price + " from " + find_source(d.buy_link)
            rel_deals.append(d_dict)

        try:
            price = d.price.replace("$", '')
            price = float(price)
        except Exception:
            price = "10% Off"

        plat = "PC"

        if "Xbox" in d.platform:
            plat = "Xbox One"
        elif "PS4" in d.platform:
            plat = "Playstation 4"

        one_deal = {"title": d.title, "cover":db_res.image, "pagelink": "https://gamescout.io/info/" + db_res.name, "genre": stolist(db_res.genre),
        "platform": plat, "story": summary, "rating": rat, "rating_count": rat_count, "price": price, "date": datetime.date.today()}

        today_deals.append(one_deal)

    if price:
        pass
    else:
        price = ""

    try:
        info_res = {"title": db_res.name, "image": db_res.image, "rating": db_res.rating, "date": db_res.release_date, "summary": db_res.summary, "story": db_res.storyline, "trailer": db_res.trailer}
    except Exception:
        info_res = {"title": "", "image": "", "rating": "", "date": "", "summary": "", "story": "", "trailer": ""}

    # strips to only leave youtube video id
    info_res["trailer"] = info_res["trailer"].replace("https://www.youtube.com/watch?v=", "")

    json_p = {"rating": rat, "rating_count": rat_count, "price": price, "date": datetime.date.today()}

    extra = content_gen.generate_text(title)

    social = {}

    url_encode = {":":"%3A", "/":"%2F", " ": "%2520"}
    game_ref_link = "https://gamescout.io/info/" + title

    for key, item in url_encode.items():
        if key in game_ref_link:
            game_ref_link = game_ref_link.replace(key, item)

    social["twitter"] = "https://twitter.com/intent/tweet?text={}".format(title + " for $" + str(extra["section_price"])) + "&url=" + game_ref_link
    social["reddit"] = "https://www.reddit.com/r/gaming/submit?url={}&title={}".format("https://gamescout.io/info/" + title, title + " for $" + str(extra["section_price"]))


    return render_template('more_info.html', json_p=json_p, extra=extra, social=social, today_deals=today_deals,title=info_res["title"], image=info_res["image"], rating=info_res["rating"], date=info_res["date"], summary=info_res["summary"], story=info_res["story"], rel_deals=rel_deals, trailer=info_res["trailer"])

@app.route('/json/<title>', methods=["GET"])
def inwindfeat(title):
    deals_DATABASE = GetDeals()
    gamextra = GetGameInfo()
    # Finds game details from deep database
    db_res = gamextra.game_info(title)
    gamextra.close_session()

    try:
        # Finds deal related to game in current db
        game_deals = deals_DATABASE.deal_info(title)
    except Exception:
        game_deals = []

    deals_DATABASE.close_session()

    # creates url to game
    url = "https://gamescout.io/info/" + title

    # updates url
    url_db = UrlUpdate()
    url_db.update_url(url)

    url_db.close_session()

    # stores dict of all deals
    rel_deals = []

    today_deals = []

    price = False

    try:
        summary = db_res.summary
        if len(summary) > 500:
            summary = summary[:500]
    except Exception:
        summary = "None"

    try:
        rat = (int(db_res.rating)/20)
    except Exception:
        rat = 3

    rat_count = randint(3, 30)

    for d in game_deals:
        try:
            d_dict = {}
            d_dict["offer_title"] = d.title
            d_dict["platform"] = d.platform
            d_dict["buylink"] = d.buy_link
            d_dict["offer_phrase"] = d.price + " from " + find_source(d.buy_link)
            rel_deals.append(d_dict)
        except Exception:
            d_dict = {}
            d_dict["offer_title"] = d.title
            d_dict["platform"] = "PC"
            d_dict["buylink"] = d.buy_link
            d_dict["offer_phrase"] = d.price + " from " + find_source(d.buy_link)
            rel_deals.append(d_dict)

        try:
            price = d.price.replace("$", '')
            price = float(price)
        except Exception:
            price = "10% Off"

        plat = "PC"

        if "Xbox" in d.platform:
            plat = "Xbox One"
        elif "PS4" in d.platform:
            plat = "Playstation 4"

        one_deal = {"title": d.title, "cover":db_res.image, "pagelink": "https://gamescout.io/info/" + db_res.name, "genre": stolist(db_res.genre),
        "platform": plat, "story": summary, "rating": rat, "rating_count": rat_count, "price": price, "date": datetime.date.today()}

        today_deals.append(one_deal)

    if price:
        pass
    else:
        price = ""

    try:
        info_res = {"title": db_res.name, "image": db_res.image, "rating": db_res.rating, "date": db_res.release_date, "summary": db_res.summary, "story": db_res.storyline, "trailer": db_res.trailer}
    except Exception:
        info_res = {"title": "", "image": "", "rating": "", "date": "", "summary": "", "story": "", "trailer": ""}

    # strips to only leave youtube video id
    info_res["trailer"] = info_res["trailer"].replace("https://www.youtube.com/watch?v=", "")

    json_p = {"rating": rat, "rating_count": rat_count, "price": price, "date": datetime.date.today()}

    extra = content_gen.generate_text(title)

    social = {}

    url_encode = {":":"%3A", "/":"%2F", " ": "%2520"}
    game_ref_link = "https://gamescout.io/info/" + title

    for key, item in url_encode.items():
        if key in game_ref_link:
            game_ref_link = game_ref_link.replace(key, item)

    soc_twit = "https://twitter.com/intent/tweet?text={}".format(title + " for $" + str(extra["section_price"])) + "&url=" + game_ref_link
    soc_red = "https://www.reddit.com/r/gaming/submit?url={}&title={}".format("https://gamescout.io/info/" + title, title + " for $" + str(extra["section_price"]))

    social["twitter"] = 'window.open("{}")'.format(soc_twit)
    social["reddit"] = 'window.open("{}")'.format(soc_red)

    json_obj = {"social": social, "image": "https://gamescout.io/" + info_res["image"], "title": info_res["title"], "date": info_res["date"], "rating": info_res["rating"], "rel_deals": rel_deals, "trailer": "https://www.youtube.com/embed/" + info_res["trailer"] + "?rel=0&amp;showinfo=0",
    "extra": extra, "summary": info_res["summary"]}

    return make_response(jsonify({"more_info": json_obj}))


@app.route('/ref/', methods=["GET"])
def ref():
    game_name = request.args.get('gimg')
    return redirect("https://gamescout.io/info/{}".format(game_name), code=301)

# Sends master json file with all deals and image locals
@app.route('/masterdeals', methods=["GET"])
def main_json():
    with open("/var/www/VgApp/vgdeals_production/Master_Deals.json", "r") as f:
        fil = json.load(f)
    return make_response(jsonify(fil), 200)

#Error Handling Unable to find endpoint
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not Found"}), 404)


@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    allurl = []
    gamed = GetDeals()
    url = gamed.uniqueurls()
    gamed.close_session()

    date = datetime.date.today()

    for u in url:
        allurl.append({"url": u, "date": date})

    return render_template('sitemap.xml', allurl=allurl)

@app.route("/robots.txt", methods=["GET"])
def robots():
    return render_template('robots.txt')



if __name__ == '__main__':
    CORS(app)
    app.run()
