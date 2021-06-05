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
