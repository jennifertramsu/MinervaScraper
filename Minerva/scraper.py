import os
import sys
import json
import pandas as pd
from dotenv import load_dotenv

# scrapers 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# email stuff
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_page():
    """ Loads the unofficial transcript in Minerva using Selenium and returns the transcript_table which will be used for scraping. """
    
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
    options.headless = True
    
    try:
        driver = webdriver.Chrome(executable_path='../chromedriver.exe', options=options)
    except:
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
    
    return driver, transcript_table

def minervascrape(values, term, year, transcript_table, terms, file):
    """ This is the main scraper function. Given the inputted terms (optional), the function will scrape through the user's
    unofficial transcript on Minerva and write the output (Course Code, Grade, Course Average, Term GPA) to a text file.
    
    Parameters
    ----------
    values : list
        List of system arguments (term + year) inputted through the command-line. If no arguments are given, 
        function will scrape for all terms.
    
    term : list
        List of specified terms represented by the first letter ('f', 'w', 's').
    
    year : list
        List of years corresponding to the specified terms. 
        
    transcript_table : list
        List of Selenium.element objects that contains all the text to be parsed and scraped.
        
    terms : dict
        Dictionary that maps the elements in term to the corresponding term name ('Fall', 'Winter', 'Summer').
        
    file : file-type
        File-type object to which the function writes.    
        
    Examples
    --------
    >> import os
    >> os.system("python minervascraper.py f2019 w2020 S2020")
    """
    
    k = 0
    d = [] # creating dictionary
    for i in range(len(transcript_table)):
        if len(values) != 0:
            if (term[k] not in transcript_table[i].text) or (year[k] not in transcript_table[i].text):
                continue
            else:
                t = term[k] + " " + year[k]
                print("Scraping " + t + "...\n")
        else: # no arguments, scrape all terms
            if (terms['F'] not in transcript_table[i].text) and (terms['W'] not in transcript_table[i].text) and (terms['S'] not in transcript_table[i].text):
                continue
            else:
                sem = transcript_table[i].text.split()
                if len(sem) == 2:
                    t = sem[0] + " " + sem[1]
                    print("Scraping " + t + "...\n")
                else:
                    continue
        # in block of desired term and year
        j = i + 5
        if j >= len(transcript_table):
            break
        while "Winter" not in transcript_table[j].text and "Fall" not in transcript_table[j].text and "Summer" not in transcript_table[j].text: # loop per line
            if "Advanced" in transcript_table[j].text:
                # grab term gpa
                l = j
                table = transcript_table[l].find_elements_by_class_name("dedefault")
                for m in range(len(table)):
                    while "TERM GPA" not in table[m].text:
                        m += 1
                    term_gpa = table[m + 1].text
                    c = {"Term GPA" : term_gpa}
                    #d.append(c)
                    break
                break               
            course_code = transcript_table[j].text
            if "RW" in transcript_table[j - 1].text:
                c = {"Term" : t, "Course Code" : course_code, "Grade" : "Not released.", "Course Average" : "Not released."}
                d.append(c)
            else:
                grade = transcript_table[j + 5].text
                course_avg = transcript_table[j + 9].text
                if len(course_avg.strip()) == 0:
                    c = {"Term" : t, "Course Code" : course_code, "Grade" : grade, "Course Average" : "Not released."}
                    d.append(c)
                else:
                    c = {"Term" : t, "Course Code" : course_code, "Grade" : grade, "Course Average" : course_avg}
                    d.append(c)
            j += 11 # move to next course code
            if j >= len(transcript_table):
                break
        i = j
        k += 1
        if len(values) != 0 and k >= len(term):
            break

    # writing to json file
    j = json.dumps(d)
    file.write(j)
    
def json2excel(file):
    ''' Converts json file to a stacked Excel file. '''
    
    df = pd.read_json(file)

    df.set_index(['Term', 'Course Code'], inplace=True)

    return df
    
def add_drop_remove(df):
    ''' For the sake of comparison, this function removes rows where both grade and course average are empty. We are only concerned with
    courses where the grade or course average has updated (i.e. are present). '''
    
    df = df[df['Grade'] != "Not released."]
    df = df[df['Course Average'] != "Not released."]
    
    return df
    
def minervaupdate(values, term, year, transcript_table, terms):
    """ If flagged through the command-line, this function will scrape for all terms and compare with the existing Scraped_Transcript_All_Terms.txt text file.
    
    Parameters
    ----------
    values : list
        List of system arguments (term + year) inputted through the command-line. If no arguments are given, 
        function will scrape for all terms.
    
    term : list
        List of specified terms represented by the first letter ('f', 'w', 's').
    
    year : list
        List of years corresponding to the specified terms. 
        
    transcript_table : list
        List of Selenium.element objects that contains all the text to be parsed and scraped.
        
    terms : dict
        Dictionary that maps the elements in term to the corresponding term name ('Fall', 'Winter', 'Summer').
          
    Returns
    -------
    change : bool 
        True if transcript has updated, otherwise False.
    """
    
    with open("Updated_Scraped_Transcript.json", "w") as file:  
        minervascrape(values, term, year, transcript_table, terms, file)
        
    old = json2excel("Scraped_Transcript_All_Terms.json")
    new = json2excel("Updated_Scraped_Transcript.json")
    
    old = add_drop_remove(old)
    new = add_drop_remove(new)
    
    changes = []
    
    if old.equals(new):
        change = False
    else:
        if not old['Grade'].equals(new['Grade']):
            changes.append('Grade')
            change = True
        if not old['Course Average'].equals(new['Course Average']):
            changes.append('Course Average')
            change = True
        else:
            change = False
            
    if change:
        os.system("cp Updated_Scraped_Transcript.json Scraped_Transcript_All_Terms.json")
    
    os.remove("Updated_Scraped_Transcript.json")
    
    return change, changes

def send_email(changes):
    
    load_dotenv()

    port = 465

    smtp_server = "smtp.gmail.com"

    sender_email = os.getenv("EMAIL")
    receiver_email = os.getenv("MYEMAIL")
    sender_email_password = os.getenv("PASS")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Minerva Transcript Update"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    text = "Your transcript has updated on Minerva! View changes below:"
    changes = "\n\t - ".join(changes)
    
    text = text + "\n\n\t - " + changes

    message.attach(MIMEText(text, 'plain'))

    context = ssl.create_default_context()
    
    if int(sys.version[0]) > 2: # version 3
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, sender_email_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

    else:
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(sender_email, sender_email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
