import gameclasses
from gameclasses import Game
from gameclasses import Developer


## This is mostly for testing purposes. Allows you to enter a game into the "database", which isn't
## really a database yet.

title = raw_input("Enter game title: ")
developers = raw_input("Enter game developer. If multiple, separate with a comma: ")
publishers = raw_input("Enter game publisher. If multiple, separate with a comma: ")
print "Select game platforms from the following list:"
print gameclasses.platform_list
platforms = raw_input("Enter game platform. If multiple, separate with a comma: ")
print "Select game technologies from the following list:"
print gameclasses.technology_list
technologies = raw_input("Enter game technology. If multiple, separate with a comma: ")
print "Select game distribution method from the following list:"
print gameclasses.distribution_list
distribution = raw_input("Enter game distribution method. If multiple, separate with a comma: ")
print "Select game categories method from the following list:"
print gameclasses.game_cat_list
game_category = raw_input("Enter game category. If multiple, separate with a comma: ")
dev_time = raw_input("Enter game development time in months: ")
release_date = raw_input("Enter game release date (YYYY-MM-DD): ")
genre = raw_input("Enter game genre: ")
url = raw_input("Enter game URL: ")

newgame = Game(title, developers, publishers, release_date, platforms, technologies, genre, dev_time, distribution, url, game_category)
