###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import unittest
import json
import requests
from bs4 import BeautifulSoup
import re

# Begin filling in instructions....
# Define NationalPark class that takes in an HTML string representing one National Park
class NationalPark():
	def __init__(self, html_string):
		# Use BeautifulSoup on HTML string
		soup = BeautifulSoup(html_string, "html.parser")
		pass

	def similar_park(self, park):
		# compares two NationalPark instances to see if they are the same park type
		pass

	def return_park_tup(self):
		# return a tuple for each instance for easy loading into database
		pass

	def __str__(self):
		pass

class Article():
	def __init__(self, html_string):
		# Use BeautifulSoup on HTML string
		pass

	def return_article_tup(self):
		pass

	def __str__(self):
		pass

# CACHE PATTERN HERE

def get_parks_data():
	# check cache/get data
	pass

def get_article_data():
	# check cache/get data
	pass

# call get_parks_data
# create list of NationalPark instances

# call get_articles_data
# create a list of Article instances

# do something with States/average temps

# create database file
# conn = sqlite3.connect('206_final_project.db')
# cur = conn.cursor()

# CREATE PARKS TABLE
# CREATE ARTICLES TABLE
# CREATE STATES TABLE

# LOAD PARKS DATA INTO TABLE
# LOAD ARTICLES DATA INTO TABLE
# LOAD STATES DATA INTO TABLE







# CLOSE DATABASE FILE
# cur.close()

# Put your tests here, with any edits you now need from when you turned them in with your project plan.
class NationalParkTest(unittest.TestCase):
	def test_constructor_park_name(self):
		test_park = NationalPark(html_string)
		self.assertEqual(type(test_park.park_name), type("Yosemite"), "Testing that park_name variable is of type string")
	def test_constructor_park_link(self):
		test_park = NationalPark(html_string)
		self.assertEqual("http" in test_park.park_link, True, "Testing that 'http' is in the park_link URL string")
	def test_constructor_park_location(self):
		test_park = NationalPark(html_string)
		self.assertEqual(len(test_park.park_location) > 0, True, "Testing that the park_location has more than one character")
	def test_get_states_1(self):
		test_park = NationalPark(html_string)
		self.assertEqual(type(test_park.get_states()), type([]), "Testing that the return type of get_states is a list")
	def test_get_states_2(self):
		test_park = NationalPark(html_string)
		self.assertEqual(type(test_park.get_states()[0]), type("String"), "Testing that the type of the first element of the list returned by get_states is a string")

class ArticleTest(unittest.TestCase):
	def test_constructor_article_title(self):
		test_article = Article(html_string)
		self.assertEqual(type(test_article.article_title), type("Title"), "Testing that article_title instance variable is of type string")
	def test_constructor_article_text(self):
		test_article = Article(html_string)
		self.assertEqual(len(test_article.article_text) > 0, True, "Testing that the article_text has more than one character")
	def test_constructor_article_descriptions(self):
		test_article = Article(html_string)
		self.assertEqual(type(test_article.article_descriptions), type("Description"), "")

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
	unittest.main(verbosity=2)

