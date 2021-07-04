# auth things
import os
import time
from scraper import load_page, minervaupdate, send_email

print("Starting configuration for Minerva transcript update!\n")
print("Checking whether Scraped_Transcript_All_Terms.json exists...\n")

if not os.path.exists("Scraped_Transcript_All_Terms.json"):
    print("Scraped_Transcript_All_Terms.json could not be found!\n")
    os.system("python minervascraper.py")
    print("The next time you call gradeupdate, the program will use this file to check for updates!")
else:
    print("Scraped_Transcript_All_Terms.json was found!\n")

    terms = {
                'F' : 'Fall',
                'W' : 'Winter', 
                'S' : 'Summer'
            }

    values = []
    term = []
    year = []

    driver, transcript_table = load_page()
    change, changes = minervaupdate(values, term, year, transcript_table, terms)

    if change:
        print("Transcript updated!\n")
        send_email(changes)
    else:
        print("No change...\n")
