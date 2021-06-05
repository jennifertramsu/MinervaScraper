import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from requests.exceptions import Timeout
from lxml import html

# auth things
import os
from dotenv import load_dotenv

URL = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin'

try:
    page = requests.get(URL, timeout=3)
    page.raise_for_status() # successful, suppress Exceptions

except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
    
except Exception as err:
    print(f'Other error occurred: {err}')
    
except Timeout:
    print("The request has timed out.")
    
else:
    print("Success!")

''' --> able to use page as boolean bc of overloading <3
if page:
    print("Success!") # 200-400
else:
    print("Not found.") # 404
'''

print(page.text)
print(page.headers) # dictionary of all headers, dictionary access is case-insensitive

# trying auth
load_dotenv()
sid = os.getenv('MCGILLID')
PIN = os.getenv('MINERVAPIN')