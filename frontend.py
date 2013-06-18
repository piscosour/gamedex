# coding=utf-8

## Web-based frontend for GameDex querying and updating.
## Uses Flask and custom GameDex classes and operations.

from flask import Flask
from flask import render_template
from flask import request

import gameclasses
import operations
from gamelist import gamedata

## Initialise Flask app

app = Flask(__name__)

## Front Page

@app.route("/")
def show_front():
    return render_template("index.html")

## Render the full list of games in the DB. Requires templating to iterate.

@app.route("/gamelist")
def show_game_list():
    global gamedata
    gen_game_data = operations.gen_game_index(gamedata)
    return render_template("gamelist.html", game_data=gen_game_data, total=len(gamedata))

## Individual game info render.

@app.route("/game/<int:game_id>")
def show_game(game_id):
    global gamedata
    for game in gamedata:
        if game_id == game.id:
            if len(game.notes) > 0:
                return render_template("game.html", selection=game, notes=True)
            else:
                return render_template("game.html", selection=game, notes=False)
    else:
        return "Game not found!"    

## POST function for adding notes (updates page after add)

@app.route("/game/<int:game_id>/addnote", methods=["POST"])
def addnote(game_id):
    global gamedata
    if request.method == "POST":
        for game in gamedata:
            if game_id == game.id:
                new_note = gameclasses.Note(body = request.form["note-body"],
                                            title = request.form["note-title"])
                game.notes = game.notes + [new_note]
                return render_template("game.html", selection=game, notes=True)

## Add game form

@app.route("/addgame", methods=["GET", "POST"])
def add_game():
    global gamedata
    if request.method == "GET":
        return render_template("addgame.html", techs=gameclasses.technology_list, 
                               platforms=gameclasses.platform_list,
                               categories=gameclasses.game_cat_list,
                               dist_options=gameclasses.distribution_list)
    elif request.method == "POST":
        new_game = gameclasses.Game(id = len(gamedata) + 1, 
                                    title = request.form["title"],
                                    developer = request.form["developer"], 
                                    publisher = request.form["publisher"], 
                                    release_date = request.form["release_date"], 
                                    platforms = request.form["platforms"], 
                                    technologies = request.form["technologies"], 
                                    genre = request.form["genre"], 
                                    dev_time = request.form["dev_time"], 
                                    distribution = request.form["distribution"], 
                                    url = request.form["url"], 
                                    game_category = request.form["category"])
        gamedata = gamedata + [new_game]
        return render_template("add-game-confirmation.html", game=new_game)


if __name__ == "__main__":
    app.debug = True
    app.run()
