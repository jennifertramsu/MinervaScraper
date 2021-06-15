# auth things
import sys
import os
from crontab import CronTab

## idea:
# --> use crontab to enable and disable the script to run on a schedule
# --> customizable?
# --> every time the script is run, the new file is compared to an existing scrapped file
# --> if diff returns nothing, no change
# --> otherwise, an update is present, send to email
# --> ideally, Linux's crontab has an option to send email, idk about Python ?-?

# running this module sets up the environment for updates
# uses Scrapped_Transcipt_All_Terms.txt as a baseline

print("Starting configuration for Minerva grade update!\n")
print("Checking whether Scraped_Transcript_All_Terms.txt exists...\n")

if not os.path.exists("Scraped_Transcript_All_Terms.txt"):
    print("Scraped_Transcript_All_Terms.txt could not be found!\n")
    os.system("python minervascraper.py")
else:
    print("Scraped_Transcript_All_Terms.txt was found!\n")

print("Starting configuration for scheduler!")

# set up times for script to call scraper

os.system("python minervascraper.py -u")