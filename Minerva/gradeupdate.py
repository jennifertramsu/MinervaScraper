# auth things
import os
import time
from datetime import datetime
from scraper import load_page, minervaupdate, send_email, json2excel, generate_html

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

@app.route('/')
def display():
    # Always display current transcript
    
    transcript = json2excel("Scraped_Transcript_All_Terms.json")
    transcript = transcript.reset_index("Term", drop=True)
    
    dis = generate_html(transcript)

    return dis

def update():
    # Open log
    if not os.path.exists("minerva_log.txt"):
        f = open("minerva_log.txt", 'w')
    else: 
        f = open("minerva_log.txt", 'a')

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    f.write(dt_string + "\n\n")

    f.write("Starting configuration for Minerva transcript update!\n")
    f.write("Checking whether Scraped_Transcript_All_Terms.json exists...\n")

    if not os.path.exists("Scraped_Transcript_All_Terms.json"):
        f.write("Scraped_Transcript_All_Terms.json could not be found!\n")
        os.system("python minervascraper.py")
        f.write("The next time you call gradeupdate, the program will use this file to check for updates!")
    else:
        f.write("Scraped_Transcript_All_Terms.json was found!\n")

        terms = {
                    'F' : 'Fall',
                    'W' : 'Winter', 
                    'S' : 'Summer'
                }

        values = []
        term = []
        year = []

        driver, transcript_table, gpa_available = load_page(f)
        change, changes = minervaupdate(values, term, year, transcript_table, gpa_available, terms)

        if change:
            f.write("Transcript updated!\n")
            send_email(changes)
        else:
            f.write("No change...\n")

    f.write("\n")

# Initialize scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(update) # Start immediately on launch
#scheduler.add_job(update, 'interval', minutes=20) # Testing scheduler after 20 minutes
scheduler.start()