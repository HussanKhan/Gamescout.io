#!/usr/bin/python3
import sys
import gzip
import shutil
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/VgApp/vgdeals_production/")

from site_scrapers.AmazonDeals import AmazonGames
from site_scrapers.CDKeysDeals import CDKEYSDEALS
from site_scrapers.HumbleDeals import HumbleBundle
from site_scrapers.BestbuyDeals import BestBuy
from site_scrapers.GamestopDeals import GameStop
from site_scrapers.RazerDeals import Razer
from game_info.GameGenre import get_details
from game_info.clean_title import clean_title as cleaner
from psqldb import GetGameInfo
from dealsdb import GetDeals

from resize import cut_images, delete_images, download_images

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_create.database_generation import Games, CommonNames
from sqlalchemy.ext.declarative import declarative_base
from LiteHandler import LiteQueryC, LiteQueryG
from QualityCheck import qualitycontrol
import json
import os
import time
from twilio.rest import Client

account = "ACe2e01506eb05a0e4b01dd8e4a4244fa5"
token = "a0b6e07d6f8e06c3516261262d41bc70"
client = Client(account, token)

message = client.messages.create(to="+12242412335", from_="+12242368932",
                                 body="Started Script")


# Needed for capturing print statements
# old_stdout = sys.stdout
#
# log_file = open("message.log","w")
#
# sys.stdout = log_file

# Querying psql databases
psql_DATABASE = GetGameInfo()
deals_DATABASE = GetDeals()

# Before starting delete all contents of database
gamedb = LiteQueryG()
gamedb.delete_all()

#Filling database with amazon deals
try:
 fill_Amazon = AmazonGames()
 fill_Amazon.parse_data()
except Exception:
 print("Problem getting deals from Amazon")

#Filling database with CDKeys deals
try:
   CDKEYSDEALS().parse_page()
   print("CD KEYS RAN")
except Exception:
   print("Problem getting deals from CDKeys")

# # # #Filling database with humblebundle deals
try:
 humble_int = HumbleBundle()
 humble_int.humble_parse()
except Exception:
 print("Problem gettings deals from HumbleBundle")

#Fill databse with gamestop deals
try:
 gamestop_int = GameStop()
 gamestop_int.gamestop_parse()
except Exception:
 print("Problem gettings deals from GameStop")
# # #
# # # #Getting deals from razer
try:
 Razer().razer_parse()
except Exception:
 print("Problem gettings deals from Razer Gamestore")

# # # #Fill datbase with besybuy deals
try:
  BestBuy().best_parse()
except Exception:
  print("Error getting games from Best Buy")


message = client.messages.create(to="+12242412335", from_="+12242368932",
                                 body="Finished Scraping")

# Deleting from psql deals VERY IMPORTANT FOR INFO SECTION
deals_DATABASE.delete_deals()

# Shows all games in database
check_games = gamedb.query_all()

# Making instance of common name mappings
c_names = LiteQueryC()

# Finds and adds proper genres to games
for lite_deal in check_games:
   # Cleans up directly copied titles from pages
    cleaner_res = cleaner(lite_deal.title)
    cleaned_title = cleaner_res[0]

    # Able to extarct platform from title
    platform = cleaner_res[1]

    # See if cleaned title exists in common names
    name_check = c_names.query_name(cleaned_title)

    deep_name_base = ""

    # IF match found
    if name_check != "NONE":

        # How game is titled in deep game database
        # Refer to it using this
        off_name = name_check.deep_name

        try:
            print("Already in DB " + off_name)
            print("REVIEW CHECK")
            psql_DATABASE.add_game_db(off_name, "", "", "", "", "", "")
        except Exception:
            print("Already in DB nonotype")

        deep_name_base = off_name

        # Retreiving data from deep database
        deep_game_data = psql_DATABASE.game_info(off_name)

        if deep_game_data != "NONE":
            # Changing genre
            gamegen = deep_game_data.genre

            if "Xbox Games" in gamegen:
                gamegen = gamegen.replace("Xbox Games", platform)
            elif "PS4 Games" in gamegen:
                gamegen = gamegen.replace("PS4 Games", platform)
            elif "Nintendo Games" in gamegen:
                gamegen = gamegen.replace("Nintendo Games", platform)
            elif "PC" in gamegen:
                gamegen = gamegen.replace("PC", platform)
            else:
                gamegen = gamegen.replace("]", ", {}]".format(platform))


            lite_deal.genre = gamegen
            lite_deal.image = deep_game_data.image
            gamedb.commit_game()

    # No match found, add to common names
    else:
        print("Adding New Entry to Deep Database")
        # Requesting data from api
        api_res_dict = get_details(cleaned_title)

        if api_res_dict != "NONE":
            # Appends array with platform name
            api_res_dict['genre'].append(platform)

            # Downloading new image, returns image url location
            img_link = str(download_images(cleaned_title, api_res_dict['image'], "Gamecovers"))
            lite_deal.image = img_link

            psql_DATABASE.add_game_db(api_res_dict['name'], api_res_dict['release_date'], img_link, api_res_dict['genre'],
            api_res_dict['rating'], api_res_dict['summary'], api_res_dict['storyline'])

            deep_name_base = api_res_dict['name']

            # Adding to common names mapping
            c_names.append_entry(cleaned_title, api_res_dict['name'])

            # Adding genres to lite deals database
            lite_deal.genre = str(api_res_dict['genre'])
            gamedb.commit_game()
            time.sleep(0.5)

    # Add to deals psql db
    deals_DATABASE.add_deal_db(lite_deal.title, lite_deal.buy_link, lite_deal.price, platform, deep_name_base)

# stores game data to be written to json
formated_games = []

message = client.messages.create(to="+12242412335", from_="+12242368932",
                                 body="Gathered data from api")

# Creating array of all games in database to append into json
for i in check_games:
    if qualitycontrol(i):
        cleaner_res = cleaner(i.title)
        cleaned_title = cleaner_res[0]

        plat = "PC"
        if "Xbox Games" in i.genre:
            plat = "XBOX"
        elif "PS4 Games" in i.genre:
            plat = "PS4"
        elif "Nintendo Games" in i.genre:
            plat = "NINTENDO"

        if i.genre == "[]":
            game_title = deals_DATABASE.search_deal(i.title)
            game_title = game_title.deep_name
            data = {"source": i.source, "title": game_title, "price": i.price, "image": i.image, "link": i.buy_link, "genre": ["Other"], "plat": plat}
        else:
            game_title = deals_DATABASE.search_deal(i.title)
            game_title = game_title.deep_name

            plain_string = i.genre.replace(']', '').replace('[', '').replace("'", '')
            plain_string = plain_string.split(',')
            cleaned_array = []
            for g in plain_string:
                cleaned_array.append(g.lstrip())
            print("Game Added")


            data = {"id": i.id, "source": i.source, "title": game_title, "genre": cleaned_array, "price": i.price, "image": i.image, "link": i.buy_link, "plat": plat}

        formated_games.append(data)

# Themes ID to theme name mappings
every_genre =  [
"Highly Rated Games",
"Recently Released Games",
"Released Last Year",
"Role-playing Games",
"Open World Games",
"Science Fiction Games",
"Racing Games",
"Strategy Games",
"Horror Games",
"Survival Games",
"Warfare Games",
"Fantasy Games",
"Other"]

# stores pairs of genre (above) and game id matches
gen_mappings = []

# Loops through eahc genre and finds matches
for gen in every_genre:
    game_ids = []
    already_inserted = []
    filtered_games = gamedb.gen_match(gen)
    for i in filtered_games:
        game_title = deals_DATABASE.search_deal(i.title)
        game_title = game_title.deep_name
        if game_title not in already_inserted:
            game_ids.append(i.id)
            already_inserted.append(game_title)

    gen_mappings.append([gen, game_ids])

# Notifies flask that updating occuring and to redirect to other page
f = open("/var/www/VgApp/vgdeals_production/UPDATING.TXT", 'w')
f.close()

# Removing older deals json
os.remove('/var/www/VgApp/vgdeals_production/Master_Deals.json')
os.remove('/var/www/VgApp/vgdeals_production/Master_Deals.json.gz')

# Creates and writes to master_deals json file
with open("/var/www/VgApp/vgdeals_production/Master_Deals.json", "w") as newfile:
    json.dump({"Deals": formated_games, "Genres": gen_mappings}, newfile)

# Gzipping file
with open('/var/www/VgApp/vgdeals_production/Master_Deals.json', 'rb') as f_in:
    with gzip.open('/var/www/VgApp/vgdeals_production/Master_Deals.json.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print("MASTER JSON HAS BEEN BUILT!")

# Deletes notification of update
os.remove('/var/www/VgApp/vgdeals_production/UPDATING.TXT')

# sys.stdout = old_stdout
#
# log_file.close()

psql_DATABASE.all_sess_close()
deals_DATABASE.all_sess_close()



deal_count = len(formated_games)

message = client.messages.create(to="+12242412335", from_="+12242368932",
                                 body="Database Succesfully Filled! There are {} deals today".format(deal_count))
