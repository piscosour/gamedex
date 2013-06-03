# coding=utf-8

## Web-based frontend for GameDex querying and updating.
## Uses Flask and custom GameDex classes and operations.

from flask import Flask
import gameclasses
from gamelist import gamedata
import operations

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello world!"
    
@app.route("/gamelist")
def game_list(data=gamedata):
    operations.game_index(data)
    return True

if __name__ == "__main__":
    app.debug = True
    app.run()
