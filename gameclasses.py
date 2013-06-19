# coding=utf-8

## These lists are not comprehensive. Maybe they shouldn't be and can be machine generated based on
## user input? Not useful for a web interface, though, unless it's a free text field.

## Also - maybe these need to go on separate files and imported on load?

## Also - think about turning them into dictionaries of key:value pairs.

import datetime

platform_list = {1:"PC", 2:"Mac", 3:"PSX", 4:"PS2", 5:"PS3", 6:"NES",
                 7:"SNES", 8:"N64", 9:"GCN", 10:"NDS", 11:"WII", 12:"GB",
                 13:"GBC", 14:"GBA", 15:"C64", 16:"Amiga", 17:"Xbox",
                 18:"Xbox 360", 19:"Genesis", 20:"Saturn", 21:"Dreamcast",
                 22:"Windows", 23:"Atari 2600", 24:"Facebook", 25:"Web",
                 26:"iOS", 27:"Android", 28:"Windows Phone"}
distribution_list = {1:"Retail", 2:"Digital", 3:"Steam", 4:"iTunes", 5:"Web",
                     6:"Xbox Live", 7:"Playstation Network", 8:"Freeware",
                     9:"Social", 10:"Google Play"}
technology_list = {1:"Unity", 2:"GameMaker", 3:"RPGMaker", 4:"Assembly",
                   5:"C/C++", 6:"BASIC", 7:"Cloud Computing", 8:"Python",
                   9:"Javascript", 10:"HTML5", 11:"Flash", 12:"Konstruct",
                   13:"Custom"}
game_cat_list = {1:"Mobile", 2:"Console", 3:"Casual", 4:"Text", 5:"Web",
                 6:"ARG", 7:"Mod", 8:"Hack", 9:"Commercial", 10:"Advergame",
                 11:"Newsgame", 12:"Serious", 13:"Learning", 14:"Conversion",
                 15:"Noncommercial", 16:"Localized", 17:"Remake", 18:"Social"}


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
            if element in platform_list.values():
                self.platforms = self.platforms + [element]
            else:
                raise ValueError("Platform not on platforms list.")

    def add_technologies(self, technologies):
        if technologies is None:
            raise ValueError("No technology specified.")
        elif self.technologies is None:
            self.technologies = []
        for element in technologies.split(","):
            if element in technology_list.values():
                self.technologies = self.technologies + [element]
            else:
                raise ValueError("Technology not on technologies list.")

    def add_game_cat(self, game_category):
        if game_category is None:
            raise ValueError("No category specified.")
        elif self.game_category is None:
            self.game_category = []
        for element in game_category.split(","):
            if element in game_cat_list.values():
                self.game_category = self.game_category + [element]
            else:
                raise ValueError("Category not on categories list.")

    def add_game_dist(self, dist_method):
        if dist_method is None:
            raise ValueError("No distribution method specified.")
        elif self.distribution is None:
            self.distribution = []
        for element in dist_method.split(","):
            if element in distribution_list.values():
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
