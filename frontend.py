# coding=utf-8

## Web-based frontend for GameDex querying and updating.
## Uses Flask and custom GameDex classes and operations.

from flask import Flask
from flask import render_template
from flask import request
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

@app.route("/addgame", methods=["GET", "POST"])
def add_game(data=gamedata):
    if request.method == "GET":
        return render_template("addgame.html")
    elif request.method == "POST":
        data = data + [Game(request.form["title"], request.form["developer"], request.form["publisher"], request.form["release_date"], request.form["platforms"], request.form["technologies"], request.form["genre", request.form["dev_time"], request.form["distribution"], request.form["url"], request.form["category"])]
        return render_template("add-game-confirmation.html", title=request.form["title"])


if __name__ == "__main__":
    app.debug = True
    app.run()
