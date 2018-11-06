from psqldb import GetGameInfo
from dealsdb import GetDeals
from stringtolist import stolist2

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

def format_plat(plat):
    plat = plat.lower()

    if "ps4" in plat:
        return "Playstation 4"
    elif "pc" in plat:
        return "PC"
    elif "xbox" in plat:
        return "Xbox One"
    elif "nintendo" in plat:
        return "Nintendo Switch"
    else:
        return "PC"

def vendor_desc(price, vendor, game):
    if "Amazon" in vendor:
        support = "Amazon is the largest online retailer in the world and their currently offering {} at the discounted price of {}.".format(game, price)
        return support
    elif "Humble Bundle" in vendor:
        support = "Humble Bundle is a trusted digital video game distributor and is beloved by the gaming community for their charity work. Humble Bundle is currently offering {} for {}.".format(game, price)
        return support
    elif "GameStop" in vendor:
        support = "GameStop is a well-known retail video game vendor, and is currently offering {} for {}.".format(game, price)
        return support
    elif "Best Buy" in vendor:
        support = "Best Buy is a popular electronics seller, and it’s currently offering {} for {}.".format(game, price)
        return support
    elif "CD Keys" in vendor:
        support = "CD Keys is a trusted video game seller and does thousands of sales everyday. The site manages to get the lowest price for games by using currency fluctuations. CD Keys is offering {} for {}".format(game, price)
        return support
    elif "Razer Gamestore" in vendor:
        support = "Razer is a popular gaming gear seller, but what a lot of people don’t know is that Razer also sells games on the Razer Gamestore. The Razer Gamestore is currently offering {} for {}.".format(game, price)
        return support

def generate_text(game_name):

    final_response = {}
    deal_from_psql = GetDeals()
    deals = deal_from_psql.deal_info(game_name)
    deal_from_psql.close_session()


    reviews = []

    if deals:
        num_deals = len(deals)

        # Stores unique vendors
        vendors = []

        # Stores unique plats
        plats = []

        # vendor support
        support_vend = []

        # stores lowest price
        low_price = 100

        for li in deals:
            vend = find_source(li.buy_link)
            if vend not in vendors:
                vend_rep = vendor_desc(li.price, vend, game_name)
                support_vend.append(vend_rep)
                vendors.append(vend)

            plat = format_plat(li.platform)
            if plat not in plats:
                plats.append(plat)

            try:
                pri = float(li.price.replace("$", ""))
                if pri < low_price:
                    low_price = pri
            except Exception:
                pass

        # SECTION 1 BASIC INFO

        # Number of deals
        if num_deals == 1:
            dis_info = "There is one deal available for {}, from {}. ".format(game_name, vendors[0])
        elif num_deals > 1:
            dis_info = "There are {} deals available for {}, from {}. ".format(num_deals, game_name, ", ".join(vendors))
        else:
            dis_info = ""

        # price for deals
        if low_price != 100:
            dis_info2 = "The current lowest price for {} is ${}. ".format(game_name, low_price)
        else:
            dis_info2 = "The current lowest price for {} is 10% off. ".format(game_name)

        # Platforms for deals
        if len(plats) == 1:
            dis_info3 = "This deal is available for the {} version of the game. ".format(plats[0])
        elif len(plats) > 1:
            dis_info3 = "These deals are available for the {} versions of the game. ".format(", ".join(plats))

        final_response["section_1"] = dis_info + dis_info2 + dis_info3

        # SECTION 2 REVIEWS
        deep_deals_info = GetGameInfo()
        deep_info = deep_deals_info.game_info(game_name)
        deep_deals_info.close_session()

        revs = stolist2(deep_info.storyline)

        revs1 = revs[2:]

        final_response["section_2"] = revs1

        # SECTION 3 VENDOR REVIEWS
        final_response["section_3"] = support_vend

        final_response["section_stock"] = "http://schema.org/InStock"

        final_response["section_price"] = low_price

        return final_response
    else:
        # SECTION 2 REVIEWS
        deep_deals_info = GetGameInfo()
        deep_info = deep_deals_info.game_info(game_name)
        deep_deals_info.close_session()

        revs = stolist2(deep_info.storyline)

        revs1 = revs[2:]
        return {"section_1": "There are no current deals for {}.".format(game_name), "section_2": revs1, "section_3":"", "section_stock":"http://schema.org/OutOfStock", "section_price": 0}
