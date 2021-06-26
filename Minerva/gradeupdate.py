# auth things
import os
import time
from scraper import *

print("Starting configuration for Minerva grade update!\n")
print("Checking whether Scraped_Transcript_All_Terms.txt exists...\n")

if not os.path.exists("Scraped_Transcript_All_Terms.txt"):
    print("Scraped_Transcript_All_Terms.txt could not be found!\n")
    os.system("python minervascraper.py")
else:
    print("Scraped_Transcript_All_Terms.txt was found!\n")

terms = {
            'F' : 'Fall',
            'W' : 'Winter', 
            'S' : 'Summer'
        }

values = []
term = []
year = []

driver, transcript_table = load_page()
change = minervaupdate(values, term, year, transcript_table, terms)

if change:
    print("Transcript updated!\n")
    send_email()
else:
    print("No change...\n")
