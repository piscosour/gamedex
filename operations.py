from gameclasses import Game
from gameclasses import Developer
from gamelist import gamelist

## List all the games in the Gamedex, with devs and year.

def game_index(data):
    for game in data:
        print game.title, "(",
        for developer in game.developer:
            print developer.name, ",",
        print game.release_date[:4], ")"
