# coding=utf-8

## Web-based frontend for GameDex querying and updating.
## Uses Flask and custom GameDex classes and operations.

from flask import Flask
import gameclasses
import gamelist
import operations

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello world!"
    
if __name__ == "__main__":
    app.run()
