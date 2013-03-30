
## These lists are not comprehensive. Maybe they shouldn't be and can be machine generated based on
## user input? Not useful for a web interface, though, unless it's a free text field.

## Also - maybe these need to go on separate files and imported on load?

## Also - think about turning them into dictionaries of key:value pairs.


platform_list = ["PC", "Mac", "PSX", "PS2", "PS3", "NES", "SNES", "N64",
                 "GCN", "NDS", "WII", "GB", "GBC", "GBA", "C64", "Amiga"]
distribution_list = ["Retail", "Digital", "Steam", "ITMS", "Web"]
technology_list = ["Unity", "GameMaker", "RPGMaker", "Assembly", "C/C++", "BASIC",
                   "Cloud Computing"]


class Game:

    """A game in the Gamedex."""

    def __init__(self, title, developer=None, publisher=None, release_date=None,
                 platforms=None, technologies=None, genre=None, build_time=None,
                 distribution=None, url=None):
        self.title = title
        if developer is not None:
            self.developer = []
            self.add_dev(developer)
        if publisher is not None:
            self.publisher = []
            self.add_pub(publisher)
        self.release_date = release_date
        if platforms is not None:
            self.platforms = []
            self.add_platform(platforms)
        self.technologies = technologies
        self.genre = genre
        self.build_time = build_time
        self.distribution = distribution
        self.url = url

    ## These functions are called independently so they can also be used to update content outside of init.
    
    def add_dev(self, developer):
        if developer is None:                   ## Are you giving me something?
            raise ValueError("No developer specified.")
        elif self.developer is None:            ## Do I have something?
            self.developer = []
        for element in developer.split(","):    ## Parse and add yours to mine.
            self.developer = self.developer + [Developer(element)]

    def add_pub(self, publisher):
        if publisher is None:
            raise ValueError("No publisher specified.")
        elif self.publisher is None:
            self.publisher = []
        for element in publisher.split(","):
            self.publisher = self.publisher + [Developer(element)]

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

class Developer:

    """A developer or publisher of a game."""

    def __init__(self, name, start_date=None, size=None, location=None,
                 end_date=None, url=None, email=None):
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
            
        

    
