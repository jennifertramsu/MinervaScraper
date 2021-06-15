# auth things
import os
import time
from app import keep_alive

keep_alive()

print("Starting configuration for Minerva grade update!\n")
print("Checking whether Scraped_Transcript_All_Terms.txt exists...\n")

if not os.path.exists("Scraped_Transcript_All_Terms.txt"):
    print("Scraped_Transcript_All_Terms.txt could not be found!\n")
    os.system("python minervascraper.py")
else:
    print("Scraped_Transcript_All_Terms.txt was found!\n")

print("Minerva Update will run in background every minute...\n")
# set up times for script to call scraper

while 1:
    os.system("python minervascraper.py -u")
    time.sleep(60)
