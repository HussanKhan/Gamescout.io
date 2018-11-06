def clean_title(game_name):
    # Default platform
    platform = "PC"

    # Lower text
    game_name = game_name.lower()

    game_name.rstrip("[")
    game_name.rstrip("(")

    # Checks if xbox keyword in title, and changes platform
    if "xbox" in game_name:
        platform = "Xbox Games"

    if "nintendo" in game_name or "switch" in game_name:
        platform = "Nintendo Games"

    # Checks if keywords for playstation in title, and changes platform
    if "playstation" in game_name or "ps4" in game_name or "psn" in game_name:
        platform = "PS4 Games"

    # Anything between [] and ()
    if "[" in game_name:
        leftside = game_name.index('[')
        rightside = game_name.index(']')
        game_name = game_name[:leftside] + game_name[rightside + 1:]
    if "(" in game_name:
        leftside = game_name.index('(')
        rightside = game_name.index(')')
        game_name = game_name[:leftside] + game_name[rightside + 1:]

    # List of words to remove
    term_remove = [
    "xbox 360",
    'standard',
    'xbox one',
    'playstation 4',
    'playstation 3',
    'windows',
    'ps4',
    '-' ,
    '/' ,
    'pc' ,
    "™",
    'digital code',
    '®',
    ':',
    '+',
    "nintendo switch",
    'nintendo',
    'xbox',
    'edition',
    'deluxe edition',
    'pack',
    'content',
    'dlc',
    'collection',
    'bundle',
    'premium',
    'deluxe',
    'legendary'
    ]

    # Goes through
    for term in term_remove:
        if term in game_name:
            game_name = game_name.replace(term, '')

    # Formats text
    name = " ".join(game_name.split())

    return [name, platform]
