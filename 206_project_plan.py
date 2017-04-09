## Your name: Stephanie Schouman
## The option you've chosen:

# Put import statements you expect to need here!
import unittest
import json
import requests
import twitter_info # Requires you to have a twitter_info file in this directory
from bs4 import BeautifulSoup
import re

# Write your test cases here.
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

## Remember to invoke all your tests...
if __name__ == "__main__":
	unittest.main(verbosity=2)