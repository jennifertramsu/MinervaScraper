# auth things
import sys
import getopt

# import custom functions
from scraper import *

arguments = sys.argv[1:]
short_options = "uh"
long_options = ["update", "help"]

# validating command-line flags and arguments
try:
    args, values = getopt.getopt(arguments, short_options, long_options) # args = flags, values = arguments
except getopt.error as e:
    print(str(e))
    sys.exit(2)

# variable declaration and prep
# CLI things
terms = {
            'F' : 'Fall',
            'W' : 'Winter', 
            'S' : 'Summer'
        }
term = []
year = []

if len(values) != 0:
    # sort by date W < S < F for a given year
    values = sorted(sorted(values, key=lambda x : x[0], reverse=True), key=lambda x : int(x[1:]))

    for arg in values:
        term.append(terms[arg[0].upper()])
        year.append(arg[1:])

if len(args) == 0: # no flags, proceed as usual
    driver, transcript_table = load_page()
    if len(values) != 0: # terms specified
        filename = "Scraped_Transcript_{}".format("_".join([term[i] + " " + year[i] for i in range(len(term))]))
        print("Beginning scraping for {}...\n".format(", ".join([term[i] + " " + year[i] for i in range(len(term))])))
        with open(filename + ".json", "w") as file:
            minervascrape(values, term, year, transcript_table, terms, file)
            print("Scraping complete! Please navigate to " + filename + ".txt to see results.")
    else: # no terms, scrape for all terms
        print("Beginning scraping for all terms...\n")
        with open("Scraped_Transcript_All_Terms.json", "w") as file:
            minervascrape(values, term, year, transcript_table, terms, file)
            print("Scraping complete! Please navigate to Scraped_Transcript_All_Terms.txt to see results.")
    driver.close()
else:
    for a, v in args:
        if a in ("-h", "--help"):
            print(minervascrape.__doc__)
        elif a in ("-u", "--update"):
            print("Starting update...\n")
            driver, transcript_table = load_page()
            change = minervaupdate(values, term, year, transcript_table, terms)
            if change:
                print("Transcript updated!\n")
                send_email()
            else:
                print("No change...\n")
            driver.close()