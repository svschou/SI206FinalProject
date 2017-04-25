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
import sqlite3

# Begin filling in instructions....
# Define NationalPark class that takes in an HTML string representing one National Park
class NationalPark():
	def __init__(self, html_string):
		# Use BeautifulSoup on HTML string
		try:
			soup = BeautifulSoup(html_string, "html.parser")

			# select the title container at the top of the page
			title_info = soup.find("div", {"class":"Hero-titleContainer clearfix"})
			self.park_name = title_info.find("a").text
			self.park_type = title_info.find("span", {"class":"Hero-designation"}).text
			self.park_location = title_info.find("span", {"class":"Hero-location"}).text
			
			desc_info = soup.find("div", {"class":"Component text-content-size text-content-style"})	
			self.park_description = desc_info.find("p").text

			link_info = soup.find_all("li", {"class":"has-sub"})
			park_link_end = link_info[0].find("a")["href"]
			self.park_link = "https://www.nps.gov" + park_link_end
		except:
			self.park_name = "Empty"
			self.park_type = "Empty"
			self.park_location = "Empty"
			self.park_description = "Empty"
			self.park_link = "Empty"

	def similar_park(self, park):
		# compares two NationalPark instances to see if they are the same park type
		if self.park_type == park.park_type:
			
			return "These parks are similar! Both " + self.park_name + " and " + park.park_name + " are a " + self.park_type + "."
		else:
			return "These parks are different! " + self.park_name + " is a " + self.park_type + ", while " + park.park_name + " is a " + park.park_type + "."

	def get_states(self):
		# use regular expressions on self.park_location to find two capital letter abbreviations or state names
		# look through dictionary of states

		state_list = []
		# if park location already a full state name
		if self.park_location in state_dict:
			# add the full state name
			state_list.append(self.park_location)
		# if the park location includes a list of abbreviations aka a comma is in the park location
		elif "," in self.park_location:
			abbrevs = re.findall("[A-Z]*[A-Z]", self.park_location)
			for abbrev in abbrevs:
				state_list.append(abbrev_dict[abbrev])
		# catching all territories/non-US states
		elif self.park_location == "Hawai'i":
			state_list.append("Hawaii")
		else:
			state_list.append(self.park_location)
		
		state_string = ""
		for state in state_list:
			state_string += state
			state_string += ", "
		return state_string[:-2]

	def return_park_tup(self):

		# return a tuple for each instance for easy loading into database
		return (self.park_name, self.park_type, self.get_states(), self.park_description, self.park_link)

class Article():
	def __init__(self, html_string):
		# Use BeautifulSoup on HTML string
		try:
			soup = BeautifulSoup(html_string, "html.parser")
			self.article_title = soup.find("h1").text
			# print(self.article_title)

			self.article_text = ""
			paragraph_text = soup.find_all("p")
			for p_text in paragraph_text:
				self.article_text += p_text.text
		except:
			self.article_title = "Empty"
			self.article_text = "Empty"


	def return_article_tup(self):
		return (self.article_title, self.article_text)


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

		html_strings = []

		resp = requests.get(base_url)
		soup = BeautifulSoup(resp.text, "html.parser")

		dropdown_menu = soup.find("ul", {"class":"dropdown-menu SearchBar-keywordSearch"})
		hrefs_list = dropdown_menu.find_all("li")

		for state_href in hrefs_list:
			state = state_href.find("a")
			res = requests.get("https://www.nps.gov"+state["href"])
			# html_strings.append(r.text)
			state_soup = BeautifulSoup(res.text, "html.parser")
			parks_list = state_soup.find_all("div", {"class":"col-md-9 col-sm-9 col-xs-12 table-cell list_left"})
			for park in parks_list:
				park_h3 = park.find("h3")
				park_link = park_h3.find("a")
				# print(park_link["href"])
				r = requests.get("https://www.nps.gov"+park_link["href"]+"index.htm")
				html_strings.append(r.text)

		CACHE_DICTION["parks_data"] = html_strings

		file_obj = open("206_final_project_cache.json", "w")
		file_obj.write(json.dumps(CACHE_DICTION))
		file_obj.close()

	return html_strings

def get_article_data():
	# check cache/get data
	if "articles_data" in CACHE_DICTION:
		print("Using cached data:	")
		html_strings = CACHE_DICTION["articles_data"]
	else:
		print("Getting new data:	")
		base_url = "https://www.nps.gov/index.htm"

		html_strings = []

		resp = requests.get(base_url)
		soup = BeautifulSoup(resp.text, "html.parser")

		medium_articles = soup.find_all("div", {"class":"Component Feature -medium"})
		for article in medium_articles:
			article_link = article.find("a")
			r = requests.get("https://www.nps.gov"+article_link["href"])
			html_strings.append(r.text)
		small_articles = soup.find_all("div", {"class":"Component Feature -small"})
		for article in small_articles:
			article_link = article.find("a")
			r = requests.get("https://www.nps.gov"+article_link["href"])
			html_strings.append(r.text)

		CACHE_DICTION["articles_data"] = html_strings

		file_obj = open("206_final_project_cache.json", "w")
		file_obj.write(json.dumps(CACHE_DICTION))
		file_obj.close()

	return html_strings

def get_states_data():
	if "states_data" in CACHE_DICTION:
		print("Using cached data:	")
		temps_dict = CACHE_DICTION["states_data"]
		# print(temps_dict)
	else:
		print("Getting new data:	")
		base_url = "https://www.currentresults.com/Weather/US/average-annual-state-temperatures.php"

		temps_dict = {}

		resp = requests.get(base_url)
		soup = BeautifulSoup(resp.text, "html.parser")

		sections = soup.find_all("table", {"class":"articletable tablecol-1-left"})
		for section in sections:
			rows = section.find_all("tr")
			for row in rows:
				state = row.find_all("td")
				state = list(state)
				try:
					state_name = state[0].text
					state_temp = state[1].text
					# Catching Hawai'i spelling
					if state_name == "Hawaii":
						state_name = "Hawai'i"
				except:
					state_name = ""
					state_temp = ""
				
				if len(state_name) > 0:
					temps_dict[state_name] = state_temp

		CACHE_DICTION["states_data"] = temps_dict

		file_obj = open("206_final_project_cache.json", "w")
		file_obj.write(json.dumps(CACHE_DICTION))
		file_obj.close()

	return temps_dict

abbrev_dict = {"AL":"Alabama", "AK":"Alaska", "AS":"American Samoa", "AZ":"Arizona", "AR":"Arkansas", "CA":"California", "CO":"Colorado", "CT":"Connecticut", "DE":"Delaware", "DC":"District of Columbia", "FL":"Florida", "GA":"Georgia", "GU":"Guam", "HI":"Hawaii", "ID":"Idaho", "IL":"Illinois", "IN":"Indiana", "IA":"Iowa", "KS":"Kansas", "KY":"Kentucky", "LA":"Louisiana", "ME":"Maine", "MD":"Maryland", "MH":"Marshall Islands", "MA":"Massachusetts", "MI":"Michigan", "FM":"Micronesia", "MN":"Minnesota", "MS":"Mississippi", "MO":"Missouri", "MT":"Montana", "NE":"Nebraska", "NV":"Nevada", "NH":"New Hampshire", "NJ":"New Jersey", "NM":"New Mexico", "NY":"New York", "NC":"North Carolina", "ND":"North Dakota", "MP":"Northern Marianas", "OH":"Ohio", "OK":"Oklahoma", "OR":"Oregon", "PW":"Palau", "PA":"Pennsylvania", "PR":"Puerto Rico", "RI":"Rhode Island", "SC":"South Carolina", "SD":"South Dakota", "TN":"Tennessee", "TX":"Texas", "UT":"Utah", "VT":"Vermont", "VA":"Virginia", "VI":"Virgin Islands", "WA":"Washington", "WV":"West Virginia", "WI":"Wisconsin", "WY":"Wyoming"}

state_dict = {}
for abbrev in abbrev_dict:
	state_dict[abbrev_dict[abbrev]] = abbrev
print(state_dict)

# call get_parks_data
html_parks = get_parks_data() # a list of html strings, each representing one park
# create list of NationalPark instances using list comphrehension
park_instances = [NationalPark(park) for park in html_parks]



park_instances_dict = {}
for park in park_instances:
	if park.park_name not in park_instances_dict:
		park_instances_dict[park.park_name] = park.return_park_tup()

sorted_park_instances_list = sorted(park_instances_dict)
sorted_park_instances_dict = {park:park_instances_dict[park] for park in sorted_park_instances_list}
# print(sorted_park_instances_dict)

# for park in park_instances:
# 	print(park.return_park_tup())

# Testing NationalPark.similar_park()
for x in range(5):
	print(park_instances[x].similar_park(park_instances[x+1]))

# Testing NationalPark.get_states()
for x in range(30):
	print(park_instances[x].get_states())

# call get_articles_data
html_articles = get_article_data()
# create a list of Article instances
article_instances = [Article(article) for article in html_articles]



# call get_states_data
state_temps = get_states_data()
# print(state_temps)
# create database file
conn = sqlite3.connect('206_final_project.db')
cur = conn.cursor()

# CREATE PARKS TABLE - similar to project 3 code
cur.execute('DROP TABLE IF EXISTS Parks')
table_spec = 'CREATE TABLE IF NOT EXISTS Parks (park_name TEXT PRIMARY KEY, park_type TEXT, park_location TEXT, park_description TEXT, park_link TEXT)'
cur.execute(table_spec)

# CREATE ARTICLES TABLE - similar to project 3 code
cur.execute('DROP TABLE IF EXISTS Articles')
table_spec = 'CREATE TABLE IF NOT EXISTS Articles (article_title TEXT PRIMARY KEY, article_text TEXT)'
cur.execute(table_spec)

# CREATE STATES TABLE - similar to project 3 code
cur.execute('DROP TABLE IF EXISTS States')
table_spec = 'CREATE TABLE IF NOT EXISTS States (state_name TEXT PRIMARY KEY, state_abbreviation TEXT, state_av_temp TEXT)'
cur.execute(table_spec)

parks_statement = 'INSERT INTO Parks VALUES (?, ?, ?, ?, ?)'
articles_statement = 'INSERT INTO Articles VALUES (?, ?)'
states_statement = 'INSERT INTO States VALUES (?, ?, ?)'

# LOAD PARKS DATA INTO TABLE
for park in sorted_park_instances_dict:
	if sorted_park_instances_dict[park][0] != "Empty":
		cur.execute(parks_statement, sorted_park_instances_dict[park])
# LOAD ARTICLES DATA INTO TABLE
for article in article_instances:
	cur.execute(articles_statement, article.return_article_tup())
# LOAD STATES DATA INTO TABLE
for state in state_temps:
	cur.execute(states_statement,(state, state_dict[state], state_temps[state]))
conn.commit()

# make queries to database



# CLOSE DATABASE FILE
cur.close()

# Put your tests here, with any edits you now need from when you turned them in with your project plan.
class NationalParkTest(unittest.TestCase):
	def test_constructor_park_name(self):
		test_park = NationalPark(html_parks[0])
		self.assertEqual(type(test_park.park_name), type("Yosemite"), "Testing that park_name variable is of type string")
	def test_constructor_park_link(self):
		test_park = NationalPark(html_parks[0])
		self.assertEqual("http" in test_park.park_link, True, "Testing that 'http' is in the park_link, because we want a URL string")
	def test_constructor_park_location(self):
		test_park = NationalPark(html_parks[2])
		self.assertEqual(len(test_park.park_location) > 0, True, "Testing that the park_location has more than one character")

	def test_similar_park_1(self):
		test_park_1 = NationalPark(html_parks[0])
		test_park_2 = NationalPark(html_parks[1])
		self.assertEqual(type(test_park_1.similar_park(test_park_2)), type(""), "Testing that the return type of similar_park is a string")
	def test_similar_park_2(self):
		test_park_1 = NationalPark(html_parks[1])
		test_park_2 = NationalPark(html_parks[2])
		self.assertEqual("These parks are" in test_park_1.similar_park(test_park_2), True, "Testing that the string returned by similar_park includes 'These parks are'")

	def test_get_states_1(self):
		test_park = NationalPark(html_parks[3])
		self.assertEqual(type(test_park.get_states()), type([]), "Testing that the return type of get_states is a list")
	def test_get_states_2(self):
		test_park = NationalPark(html_parks[0])
		self.assertEqual(len(test_park.get_states()) > 0, True, "Testing that the type of the first element of the list returned by get_states is a string")

	def test_return_park_tup_type(self):
		test_park = NationalPark(html_parks[0])
		self.assertEqual(type(test_park.return_park_tup()), type(()), "Testing that the type of the return value for return_park_tup is a tuple")
	def test_return_park_tup_len(self):
		test_park = NationalPark(html_parks[1])
		self.assertEqual(len(test_park.return_park_tup()), 5, "Testing that there are 5 items in the tuple returned by return_park_tup")

class ArticleTest(unittest.TestCase):
	def test_constructor_article_title(self):
		test_article = Article(html_articles[0])
		self.assertEqual(type(test_article.article_title), type("Title"), "Testing that article_title instance variable is of type string")
	def test_constructor_article_text(self):
		test_article = Article(html_articles[1])
		self.assertEqual(len(test_article.article_text) > 0, True, "Testing that the article_text has more than one character")

	def test_return_article_tup_1(self):
		test_article = Article(html_articles[2])
		self.assertEqual(type(test_article.return_article_tup()),type(()), "Testing that the type of the return value for return_article_tup is a tuple")
	def test_return_article_tup_2(self):
		test_article = Article(html_articles[0])
		self.assertEqual(len(test_article.return_article_tup()), 2, "Testing that there are 2 items in the tuple returned by return_article_tup")


class get_parks_dataTest(unittest.TestCase):
	def test_get_parks_data_1(self):
		self.assertEqual(type(get_parks_data()), type([]), "Testing that the return value of get_parks_data is a list")
	def test_get_parks_data_2(self):
		self.assertEqual(type(get_parks_data()[0]), type(""), "Testing that the type of first value returned by get_parks_data is a string (an HTML string)")

class get_article_dataTest(unittest.TestCase):
	def test_get_article_data_1(self):
		self.assertEqual(type(get_article_data()), type([]), "Testing that the return value of get_article_data is a list")
	def test_get_article_data_2(self):
		self.assertEqual(type(get_article_data()[0]), type(""), "Testing that the type of first value returned by get_article_data is a string (an HTML string)")

class get_states_dataTest(unittest.TestCase):
	def test_get_states_data_1(self):
		self.assertEqual(type(get_states_data()), type({}), "Testing that the return value of get_states_data is a dictionary")
	def test_get_states_data_2(self):
		self.assertEqual(type(get_states_data()["Michigan"]), type(""), "Testing that the value for Michigan in the temps dictionary returned by get_states_data is a string")
	def test_get_states_data_3(self):
		self.assertEqual(get_states_data()["Michigan"], "44.4", "Testing that the value for the Michigan key in the temps dictionary returned by get_states_data is 44.4")

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
	unittest.main(verbosity=2)

