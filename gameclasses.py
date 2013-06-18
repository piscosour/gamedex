# coding=utf-8

## These lists are not comprehensive. Maybe they shouldn't be and can be machine generated based on
## user input? Not useful for a web interface, though, unless it's a free text field.

## Also - maybe these need to go on separate files and imported on load?

## Also - think about turning them into dictionaries of key:value pairs.

import datetime

platform_list = ["PC", "Mac", "PSX", "PS2", "PS3", "NES", "SNES", "N64",
                 "GCN", "NDS", "WII", "GB", "GBC", "GBA", "C64", "Amiga",
                 "Xbox", "Xbox 360", "Genesis", "Saturn", "Dreamcast",
                 "Windows", "Atari 2600", "Facebook", "Web"]
distribution_list = ["Retail", "Digital", "Steam", "ITMS", "Web", "Xbox Live", "Playstation Network",
                     "Freeware", "Social"]
technology_list = ["Unity", "GameMaker", "RPGMaker", "Assembly", "C/C++", "BASIC",
                   "Cloud Computing", "Python", "Javascript", "HTML5", "Flash", "Konstruct"]
game_cat_list = ["Mobile", "Console", "Casual", "Text", "Web", "ARG", "Mod", "Hack", "Commercial",
                 "Advergame", "Newsgame", "Serious", "Learning", "Conversion", "Noncommercial",
                 "Localized", "Remake", "Social"]


class Game:

    """A game in the Gamedex."""

    def __init__(self, id, title, developer=None, publisher=None, release_date=None,
                 platforms=None, technologies=None, genre=None, dev_time=None,
                 distribution=None, url=None, game_category=None):
        self.id = id
        self.title = title
        self.developer = developer
        self.publisher = publisher
        self.release_date = release_date
        if platforms is not None:
            self.platforms = []
            self.add_platform(platforms)
        if technologies is not None:
            self.technologies = []
            self.add_technologies(technologies)
        self.genre = genre
        self.dev_time = dev_time 
        if distribution is not None:
            self.distribution = []
            self.add_game_dist(distribution)
        if game_category is not None:
            self.game_category = []
            self.add_game_cat(game_category)
        self.url = url
        self.notes = []

    ## These functions are called independently so they can also be used to update content outside of init.
    
    def add_dev(self, org_id):
        if org_id is None:                   ## Are you giving me something?
            raise ValueError("No Org specified.")
        elif self.developer is None:            ## Do I have something?
            self.developer = []
        self.developer = self.developer + [org_id]
        
    def add_pub(self, org_id):
        if org_id is None:
            raise ValueError("No publisher specified.")
        elif self.publisher is None:
            self.publisher = []
        self.publisher = self.publisher + [org_id]

    def add_platform(self, platforms):
        if platforms is None:
            raise ValueError("No platform specified.")
        elif self.platforms is None:
            self.platforms = []
        for element in platforms.split(","):
            if element in platform_list:
                self.platforms = self.platforms + [element]
            else:
                raise ValueError("Platform not on platforms list.")

    def add_technologies(self, technologies):
        if technologies is None:
            raise ValueError("No technology specified.")
        elif self.technologies is None:
            self.technologies = []
        for element in technologies.split(","):
            if element in technology_list:
                self.technologies = self.technologies + [element]
            else:
                raise ValueError("Technology not on technologies list.")

    def add_game_cat(self, game_category):
        if game_category is None:
            raise ValueError("No category specified.")
        elif self.game_category is None:
            self.game_category = []
        for element in game_category.split(","):
            if element in game_cat_list:
                self.game_category = self.game_category + [element]
            else:
                raise ValueError("Category not on categories list.")

    def add_game_dist(self, dist_method):
        if dist_method is None:
            raise ValueError("No distribution method specified.")
        elif self.distribution is None:
            self.distribution = []
        for element in dist_method.split(","):
            if element in distribution_list:
                self.distribution = self.distribution + [element]
            else:
                raise ValueError("Distribution method not on methods list.")

    def add_note(self, note):
        self.notes = self.notes + [note]

## Using Org class for both Orgs and publishers. Maybe rename to Org?

## Also - add class for individuals, for detailed team lists working on games?
            
class Org:

    """A Org or publisher of a game."""

    def __init__(self, id, name, start_date=None, size=None, location=None,
                 end_date=None, url=None, email=None):
        self.id = id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.size = size
        self.location = location
        self.url = url
        self.email = email
        if self.end_date is None:               ## If no end date indicated, assume org is still active.
            self.status = "Active"
        else:
            self.status = "Inactive"
        self.notes = []
        self.events = []

    def add_note(self, note):
        self.notes = self.notes + [note]

    def add_event(self, event):
        self.events = self.events + [event]

## For adding ongoing notes to either Games or Orgs, with title, body and timestamp.

class Note:

    """A Note with additional text information."""
    
    def __init__(self, body, title=None):
        self.title = title
        self.body = body
        self.timestamp = datetime.datetime.now()
        self.timestamp_str = str(self.timestamp)
        self.private = None

## Tracks milestones and events related to Orgs

class Event:
    """An event in an organisation's history."""

    def __init__(self, text, date, category):
        self.text = text
        self.date = date
        self.category = category
        self.private = None
