# auth things
import sys
import os
import getopt
from dotenv import load_dotenv

# scrappers 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import custom function
from scrapper import minervascrape

# loading Minerva credentials
load_dotenv()

# choosing login method --> 1 : ID login, 0 : email login
login_by_ID = int(os.getenv('LOGIN'))

if login_by_ID:
    sid = os.getenv('MCGILLID')
    pin = os.getenv('MINERVAPIN')
    
else:
    username = os.getenv('MCGILLUSERNAME')
    password = os.getenv('MCGILLPASSWORD') 

# initialize Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='../chromedriver', options=options)

# heading to Minerva login page
URL = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin'
driver.get(URL)

# wait for page to load
WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.ID, "UserID")))

if login_by_ID:
    # retrieving username field and sending username
    driver.find_element_by_id("UserID").send_keys(sid)

    # retrieving password field and sending passowrd
    driver.find_element_by_id("PIN").send_keys(pin)
    
    # clicking login button
    driver.find_element_by_id("mcg_id_submit").click()
    
else:
    # retrieving username field and sending username
    driver.find_element_by_id("mcg_un").send_keys(username)

    # retrieving password field and sending passowrd
    driver.find_element_by_id("mcg_pw").send_keys(password)

    # clicking login button
    driver.find_element_by_id("mcg_un_submit").click()

# dealing with incorrect credentials (verifying successful login)

# waiting for page to load --> execute_script executes JS code
# --> waits until the JS code returns True when page is loaded
WebDriverWait(driver=driver, timeout=10).until(
  lambda x : x.execute_script("return document.readyState === 'complete'")
)

try:
    errors = driver.find_element_by_name("web_stop")
    print("Login failed.\n")
    
except: # login successful
    print("Login successful!\n")   
    
# navigate to Unofficial Transcript
main = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_GenMenu?name=bmenu.P_StuMainMnu'
records = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_GenMenu?name=bmenu.P_AdminMnu'
transcript = 'https://horizon.mcgill.ca/pban1/bzsktran.P_Display_Form?user_type=S&tran_type=V'

navigation = [main, records, transcript]

for link in navigation:
    driver.get(link)
    WebDriverWait(driver=driver, timeout=10).until(lambda x : x.execute_script("return document.readyState === 'complete'"))

# scrape for grades
transcript_table = driver.find_elements_by_class_name("dedefault")

# CLI things
terms = {
    'F' : 'Fall',
    'W' : 'Winter', 
    'S' : 'Summer'
}

term = []
year = []

arguments = sys.argv[1:]
short_options = "u"
long_options = ["update"]

# validating command-line flags and arguments
try:
      args, values = getopt.getopt(arguments, short_options, long_options)
except getopt.error as e:
      print(str(e))
      sys.exit(2)

if len(values) != 0:
    # sort by date W < S < F for a given year
    values = sorted(sorted(values, key=lambda x : x[0], reverse=True), key=lambda x : int(x[1:]))

    for arg in values:
        term.append(terms[arg[0].upper()])
        year.append(arg[1:])

if len(args) == 0:
    if len(values) != 0:
        filename = "Scrapped_Transcript_{}".format("_".join([term[i] + " " + year[i] for i in range(len(term))]))
        print("Beginning scrapping for {}...\n".format(", ".join([term[i] + " " + year[i] for i in range(len(term))])))
        with open(filename + ".txt", "w") as file:
            minervascrape(values, term, year, transcript_table, terms, file)
            print("Scrapping complete! Please navigate to " + filename + ".txt to see results.")
    else:
        print("Beginning scrapping for all terms...\n")
        with open("Scrapped_Transcript_All_Terms.txt", "w") as file:
            minervascrape(values, term, year, transcript_table, terms, file)
            print("Scrapping complete! Please navigate to Scrapped_Transcript_All_Terms.txt to see results.")
else:
    for a, v in args:
        if a in ("-u", "--update"):
            print("Starting update...")
    
driver.close()