# auth things
import sys
import os
from dotenv import load_dotenv

# scrappers 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# loading email credentials
load_dotenv()

email = os.getenv('EMAIL')
password = os.getenv('PASS')

# initialize Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='../chromedriver', options=options)

# heading to email login page
URL = 'https://accounts.google.com/signin/v2/identifier?service=mail&passive=true&rm=false&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
driver.get(URL)

# wait for page to load
WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.ID, "logo")))

# retrieving username field and sending username
driver.find_element_by_id("identifierId").send_keys(email)
