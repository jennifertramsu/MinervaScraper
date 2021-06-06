# auth things
import os
from dotenv import load_dotenv

# scrappers 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# loading credentials
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

error_message = "Invalid McGill ID or PIN."

try:
    errors = driver.find_element_by_name("web_stop")
    print("Login failed.")
    
except: # login successful
    print("Login successful!")   
    
# navigate to Unofficial Transcript

main = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_GenMenu?name=bmenu.P_StuMainMnu'
records = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_GenMenu?name=bmenu.P_AdminMnu'
transcript = 'https://horizon.mcgill.ca/pban1/bzsktran.P_Display_Form?user_type=S&tran_type=V'

navigation = [main, records, transcript]

for link in navigation:
    driver.get(link)
    WebDriverWait(driver=driver, timeout=10).until(lambda x : x.execute_script("return document.readyState === 'complete'"))

# scrape for grades
# ideally, use from command-line (F2019, W2019, etc.)
# --> option to choose term?
# include CGPA

transcript_table = driver.find_elements_by_class_name("dedefault")

# test
term, year = ['Fall', 'Winter'], ['2019', '2021']

k = 0

for i in range(len(transcript_table)):
    if (term[k] not in transcript_table[i].text) or (year[k] not in transcript_table[i].text):
        continue
    print(term[k], year[k])
    # in block of desired term and year
    j = i + 5
    while "Winter" not in transcript_table[j].text and "Fall" not in transcript_table[j].text and "Summer" not in transcript_table[j].text: # loop per line
        if "Advanced" in transcript_table[j].text:
            break
        course_code = transcript_table[j].text
        grade = transcript_table[j + 5].text
        print(course_code, grade)
        j += 11 # move to next course code
    i = j
    k += 1
    if k >= len(term):
        break

driver.close()