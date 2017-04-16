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
		text_info = soup.find_all("div", {"class":"col-md-9 col-sm-9 col-xs-12 table-cell list_left"})
		for park in text_info:
			self.park_name = park.find("h3").text
			self.park_type = park.find("h2").text
			self.park_location = park.find("h4").text
			self.park_description = park.find("p").text
		link_info = soup.find_all("div", {"class":"col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right"})
		for park in link_info:
			print(park.find_all("a")[0]["href"])

	def similar_park(self, park):
		# compares two NationalPark instances to see if they are the same park type
		pass

	def return_park_tup(self):
		# return a tuple for each instance for easy loading into database
		return (self.park_name, self.park_type, self.park_location, self.park_description, self.park_link)

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

CACHE_FNAME = "206_final_project_cache.json"
# Put the rest of your caching setup here:

try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

def get_parks_data():
	if "parks_data" in CACHE_DICTION:
		print("Using cached data:	")
		html_strings = CACHE_DICTION["parks_data"]
	else:
		print("Getting new data:	")
		base_url = "https://www.nps.gov/index.htm"

		resp = requests.get(base_url)
		soup = BeautifulSoup(resp.text, "html.parser")

		dropdown_menu = soup.find("ul", {"class":"dropdown-menu SearchBar-keywordSearch"})
		hrefs_list = dropdown_menu.find_all("li")
		
		html_strings = []

		for state_href in hrefs_list:
			state = state_href.find("a")
			r = requests.get("https://www.nps.gov"+state["href"])
			html_strings.append(r.text)


		CACHE_DICTION["parks_data"] = html_strings

		file_obj = open("206_final_project_cache.json", "w")
		file_obj.write(json.dumps(CACHE_DICTION))
		file_obj.close()

	# state_href = hrefs_list[0].find("a")
	# r = requests.get("https://www.nps.gov" + state_href["href"])
	# print(r.text)

	return html_strings

def get_article_data():
	# check cache/get data
	pass

# call get_parks_data
# a list of html strings, each representing one state
html_parks = get_parks_data()

# print(html_parks)
# create list of NationalPark instances
# test_park = NationalPark(html_parks[0])

park_instances = []

# loop through each state html string
for state in html_parks:
	soup = BeautifulSoup(state, "html.parser")
	park_list = soup.find_all("li", {"class":"clearfix"})
	# loop through each park
	for park in park_list:
		temp_park = NationalPark(str(park)) 
		park_instances.append(temp_park)


# soup = BeautifulSoup(html_parks[0], "html.parser")
# parks_list = soup.find_all("li", {"class":"clearfix"})
# # print("FIRST PARK:	\n" parks_list[0])
# print(type(str(parks_list[0])))

# test_park = NationalPark(str(parks_list[0]))
# print(test_park.park_name+"\n"+test_park.park_type+"\n"+test_park.park_location+test_park.park_description+"\n"+test_park.park_link)

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
	def test_return_park_tup_type(self):
		test_park = NationalPark(html_string)
		self.assertEqual(type(test_park.return_park_tup()), type(()), "Testing that the type of the return value for return_park_tup is a tuple")
	def test_return_park_tup_len(self):
		test_park = NationalPark(html_string)
		self.assertEqual(len(test_park.return_park_tup()), 5, "Testing that there are 5 items in the tuple return")

class ArticleTest(unittest.TestCase):
	def test_constructor_article_title(self):
		test_article = Article(html_string)
		self.assertEqual(type(test_article.article_title), type("Title"), "Testing that article_title instance variable is of type string")
	def test_constructor_article_text(self):
		test_article = Article(html_string)
		self.assertEqual(len(test_article.article_text) > 0, True, "Testing that the article_text has more than one character")
	def test_constructor_article_descriptions(self):
		test_article = Article(html_string)
		self.assertEqual(type(test_article.article_descriptions), type("Description"), "Testing that the article_description is of type string")

class get_parks_dataTest(unittest.TestCase):
	def test_get_parks_data_1(self):
		self.assertEqual(type(get_parks_data()), type([]), "Testing that the return value of get_parks_data is a list")
	def test_get_parks_data_2(self):
		self.assertEqual(type(get_parks_data()[0]), type(""), "Testing that the type of first value returned by get_parks_data is a string (an HTML string)")

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
	unittest.main(verbosity=2)

