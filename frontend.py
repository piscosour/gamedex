# coding=utf-8

## Web-based frontend for GameDex querying and updating.
## Uses Flask and custom GameDex classes and operations.

from flask import Flask
from flask import render_template
import gameclasses
from gamelist import gamedata
import operations

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello world!"

## Render the full list of games in the DB. Requires templating to iterate.

@app.route("/gamelist")
def show_game_list():
    gen_game_data = operations.gen_game_index()
    return render_template("gamelist.html", game_data=gen_game_data)

## Individual game info render.

@app.route("/game/<int:game_id>")
def show_game(game_id, data=gamedata):
    for game in data:
        if game_id == game.id:
            return render_template("game.html", selection=game)
    else:
        return False

## Add game form

@app.route("/addgame")
def add_game():
    return render_template("addgame.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
