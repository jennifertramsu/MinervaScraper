import requests
from bs4 import BeautifulSoup

#import pprint # pretty-printing

# static HTML page
URL = 'https://www.monster.com/jobs/search/?=Software-Developer&where=Australia'

# HTTP request to the URL, retrieves HTML data and stores in object
# can print contents with the content attribute
page = requests.get(URL)

# creating the Beautiful Soup object
soup = BeautifulSoup(page.content, 'lxml')

print(soup.title)
print(soup.title.name) # pritns tag (title)
print(soup.title.string) # prints webpage name
print(soup.title.parent.name) # prints tag of parent structure (head)
# print(soup.div.prettify())
# print(soup.find_all('a')) # returns a list containing all HTML structures inside the inputed tag

# the id attribute maeks the element uniquely identifiable on the page
# other identifiers include class and name
results = soup.find(class_='results-page container')

print(results.prettify())

############################################

# with authentification

# create a Session object to persist the user session

s = requests.Session()

# getting the data we need
# --> the URL to which the POST request (sign in) will be sent
# --> the payload

# --> go to login page
# --> in developer tools, clear Network, login, then select 'session'
# --> under Headers, can retrieve URL
# --> right-click on session and select Copy as cURL (bash)
# --> go to curl.trillworks.com and paste in request data

import os
from dotenv import load_dotenv

load_dotenv()

LOGIN=os.getenv('LOGIN')
PASS=os.getenv('PASS')

data = {
  'commit': 'Sign in',
  'authenticity_token': 'eG2s9x3wNfBu6f7c2LeEA9/oqz2btBQNnk3570c7Uf8U+3h+32VuC3hEj2DAKmRx+MCZTD1NeVIkjF896X8Cug==',
  'login': LOGIN,
  'password': PASS,
}

URL = 'https://github.com/session'

response = s.post(URL, data=data)
print(response.text)
