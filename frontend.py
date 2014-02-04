# coding=utf-8

## Web-based frontend for GameDex querying and updating.
## Uses Flask and custom GameDex classes and operations.

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

from gameclasses import Game, Org
import operations
import sqlite3
import datetime
from gamelist import gamedata
from orglist import orgdata

## Config
DATABASE = "gamedex.db"
DEBUG = True
SECRET_KEY = 'development'
USERNAME = 'admin'
PASSWORD = 'default'

## Initialise Flask app

app = Flask(__name__)
app.config.from_object(__name__)

user_authenticate = True
password = "password"


##############
## DB Stuff ##
##############

## Initiate schema

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


###########
## Views ##
###########

## Front Page

@app.route("/")
def show_front():
    total_games = len(gamedata)
    total_orgs = len(orgdata)

    # platform_count = {}

    # for platform in gameclasses.platform_list.keys():
    #     counter = 0

    #     for game in gamedata:
    #         if platform in list(game.platforms):
    #             counter = counter + 1

    #     platform_count[platform] = counter

    # platform_max = platform_count[max(platform_count.values())]

    # platform_choice = gameclasses.platform[platform_max]

    return render_template("index.html", auth=user_authenticate, message=None, games=total_games, orgs=total_orgs)

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
    game = fetch_game(game_id)
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
                                   dist_options=gameclasses.distribution_list,
                                   orgs=orgdata, auth=user_authenticate)
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
        return render_template("game.html", selection=new_game, notes=False,
                               message="Game added successfully!",
                               auth=user_authenticate)

## Generate index of organisations

@app.route("/orgindex")
def show_org_list():
    return render_template("orgindex.html", org_data=orgdata, auth=user_authenticate)

## Individual org info render

@app.route("/org/<int:org_id>")
def show_org(org_id):
    org = fetch_org(org_id)
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
        return render_template("org.html", selection=new_org, notes=False,
                               game_data=gamedata, auth=user_authenticate,
                               message="Organisation added successfully!",
                               events=False)

## About page

@app.route("/about")
def about_page():
    return render_template("about.html", auth=user_authenticate)

## Helper functions

def fetch_game(id):
    ## Parses through games db, returns Game object for render/edit
    cur = g.db.execute('select * from games where id = ?', [id])
    result = cur.fetchall()
    data = result[0]
    game = Game(data[0], data[1], data[2], data[3], data[4], data[5],
                data[6], data[7], data[8], data[9], data[10], data[11])
    game.notes = fetch_notes('game', id)

    return game

def fetch_org(id):
    ## Parses through orgs db, returns Org object for render
    cur = g.db.execute('select * from orgs where id = ?', [id])
    result = cur.fetchall()
    data = result[0]
    org = Org(data[0], data[1], data[2], data[3], data[4], data[5],
                data[6], data[7], data[8])
    org.notes = fetch_notes('org', id)
    org.events = fetch_events(id)

    return org

def fetch_notes(ref_type, id):
    ## Parses through notes table, returns list of notes ##
    cur = g.db.execute('select * from notes where id = ? and ref_type = ?', [id, ref_type])
    notes = []
    for row in cur.fetchall():
        notes.append(Note(row[1], row[2], row[3], str(row[3]), row[4]))
    return notes

def fetch_events(id):
    ## Parses through events table, returns list of events ##
    cur = g.db.execute('select * from events where id = ?', [id])
    events = []
    for row in cur.fetchall():
        events.append(Event(row[1], row[2], row[3], row[4]))
    return events

##################
## Main Section ##
##################

if __name__ == "__main__":
    app.debug = True
    app.run()
