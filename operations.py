from gameclasses import Game
from gameclasses import Org
from gamelist import gamedata

## List all the games in the Gamedex, with devs and year.

def game_index(data):
    for game in data:
        print game.title, "(",
        for developer in game.developer:
            print developer.name, ",",
        print game.release_date[:4], ")"

def games_per_year(data):
    year_list = []

    for game in data:
        if game.release_date is not None:
            for year in year_list:
                if game.release_date[:4] == year[0]:
                    year = (year[0], year[1] + 1)
            else:
                year_list.append((game.release_date[:4], 1))

    return year_list
