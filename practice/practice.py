import requests
from bs4 import BeautifulSoup
'''
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

import os
from dotenv import load_dotenv

load_dotenv()

# loading credentials
username = os.getenv('LOGIN')
password = os.getenv('PASS')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait

# initialize Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='../chromedriver', options=options)

# heading to github login page
URL = "https://github.com/login"
driver.get(URL)

# retrieving username field and sending username
driver.find_element_by_id("login_field").send_keys(username)

# retrieving password field and sending passowrd
driver.find_element_by_id("password").send_keys(password)

# clicking login button
driver.find_element_by_name("commit").click()

# dealing with incorrect credentials (verifying successful login)

# waiting for page to load --> execute_script executes JS code
# --> waits until the JS code returns True when page is loaded
WebDriverWait(driver=driver, timeout=10).until(
  lambda x : x.execute_script("return document.readyState === 'complete'")
)

error_message = "Incorrect username or password."

errors = driver.find_element_by_class_name("flash-error")

# if we find that error message within errors, then login is failed
if error_message in errors.text:
      print("Login failed.")
else:
      print("Login successful!")
      
driver.close()

#####################################

# flag arguments in command-line

import sys
import getopt

arguments = sys.argv[1:]

short_options = "u"

long_options = ["update"]

try:
      args, values = getopt.getopt(arguments, short_options, long_options)
except getopt.error as e:
      print(str(e))
      sys.exit(2)
      
print(args, values)
      
for a, v in args:
      if a in ("-u", "--update"):
            print("Starting update...")
'''

######################################

# email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from dotenv import load_dotenv
import os

load_dotenv()

port = 465

smtp_server = "smtp.gmail.com"

sender_email = os.getenv("EMAIL")
receiver_email = "jennifer.tramsu@gmail.com"
sender_email_password = os.getenv("EMAILPASS")

message = MIMEMultipart("alternative")
message["Subject"] = "Test"
message["From"] = sender_email
message["To"] = receiver_email

text = open("../Minerva/Scrapped_Transcript_All_Terms.txt").read()

message.attach(MIMEText(text, 'plain'))

context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, sender_email_password)
      server.sendmail(
            sender_email, receiver_email, message.as_string()
      )
