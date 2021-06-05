import requests
from bs4 import BeautifulSoup

#import pprint # pretty-printing

# static HTML page
URL = 'https://www.monster.com/jobs/search/?=Software-Developer&where=Australia'

# HTTP request to the URL, retrieves HTML data and stores in object
# can print contents with the content attribute
page = requests.get(URL)

# creating the Beautiful Soup object
soup = BeautifulSoup(page.content, 'html-parser')

# the id attribute maeks the element uniquely identifiable on the page