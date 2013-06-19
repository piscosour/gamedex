# coding=utf-8

## Web-based frontend for GameDex querying and updating.
## Uses Flask and custom GameDex classes and operations.

from flask import Flask
from flask import render_template
from flask import request

import gameclasses
import operations
from gamelist import gamedata
from orglist import orgdata

## Initialise Flask app

app = Flask(__name__)
user_authenticate = True
password = "password"

## Front Page

@app.route("/")
def show_front():
    return render_template("index.html", auth=user_authenticate, message=None)

@app.route("/login", methods=["POST"])
def login():
    global user_authenticate
    if request.method == "POST":
        if request.form["password"] == password:
            user_authenticate = True
            return render_template("index.html", auth=user_authenticate, message=None)
        else:
            return render_template("index.html", auth=user_authenticate, message="Password incorrect.")
    
@app.route("/logout")
def logout():
    global user_authenticate
    user_authenticate = False
    return render_template("index.html", auth=user_authenticate, message="Session closed.")

## Render the full list of games in the DB. Requires templating to iterate.

@app.route("/gameindex")
def show_game_list():
    return render_template("gameindex.html", auth=user_authenticate, game_data=gamedata, total=len(gamedata))

## Individual game info render.

@app.route("/game/<int:game_id>")
def show_game(game_id):
    global gamedata
    for game in gamedata:
        if game_id == game.id:
            if len(game.notes) > 0:
                note_check = True
            else:
                note_check = False
            return render_template("game.html", selection=game,
                                   notes=note_check, org_data=orgdata, 
                                   auth=user_authenticate,
                                   techs=gameclasses.technology_list, 
                                   platforms=gameclasses.platform_list,
                                   categories=gameclasses.game_cat_list,
                                   dist_options=gameclasses.distribution_list)
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
                return render_template("game.html", selection=game, notes=True, auth=user_authenticate)

## Add game form

@app.route("/addgame", methods=["GET", "POST"])
def add_game():
    global gamedata
    if request.method == "GET":
        if user_authenticate is not True:
            return render_template("index.html", auth=user_authenticate, message="You need to log in to add games.")
        else:
            return render_template("addgame.html", techs=gameclasses.technology_list, 
                                   platforms=gameclasses.platform_list,
                                   categories=gameclasses.game_cat_list,
                                   dist_options=gameclasses.distribution_list, orgs=orgdata, auth=user_authenticate)
    elif request.method == "POST":
        new_game = gameclasses.Game(id = len(gamedata) + 1, 
                                    title = request.form["title"],
                                    developer = request.form.getlist("developer"), 
                                    publisher = request.form.getlist("publisher"), 
                                    release_date = request.form["release_date"], 
                                    platforms = request.form.getlist("platforms"), 
                                    technologies = request.form.getlist("technologies"), 
                                    genre = request.form["genre"], 
                                    dev_time = request.form["dev_time"], 
                                    distribution = request.form.getlist("distribution"), 
                                    url = request.form["url"], 
                                    game_category = request.form.getlist("category"))
        gamedata = gamedata + [new_game]
        return render_template("add-game-confirmation.html", game=new_game, auth=user_authenticate)

## Generate index of organisations

@app.route("/orgindex")
def show_org_list():
    return render_template("orgindex.html", org_data=orgdata, auth=user_authenticate)

## Individual org info render

@app.route("/org/<int:org_id>")
def show_org(org_id):
    for org in orgdata:
        if org_id == org.id:
            if len(org.notes) > 0:
                note_check = True
            else:
                note_check = False
            if len(org.events) >0:
                event_check = True
            else:
                event_check = False
            return render_template("org.html", selection=org, notes=note_check,
                                   game_data=gamedata, auth=user_authenticate,
                                   events=event_check)
    else:
        return "Organisation not found!"    

@app.route("/addorg", methods=["GET", "POST"])
def add_org():
    global orgdata
    if request.method == "GET":
        if user_authenticate is not True:
            return render_template("index.html", auth=user_authenticate, message="You need to log in to add orgs.")
        else:
            return render_template("addorg.html", orgs=orgdata, auth=user_authenticate)
    elif request.method == "POST":
        if request.form["end_date"] == "":
            end_date_check = None
        else:
            end_date_check = request.form["end_date"] 
        new_org = gameclasses.Org(id = len(gamedata) + 1, 
                                  name = request.form["name"],
                                  start_date = request.form["start_date"], 
                                  end_date = end_date_check, 
                                  size = request.form["size"], 
                                  location = request.form["location"], 
                                  url = request.form["url"], 
                                  email = request.form["email"])
        orgdata = orgdata + [new_org]
        return render_template("add-org-confirmation.html", org=new_org, auth=user_authenticate)

## About page

@app.route("/about")
def about_page():
    return render_template("about.html", auth=user_authenticate)

if __name__ == "__main__":
    app.debug = True
    app.run()
