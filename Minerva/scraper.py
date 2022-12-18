import os
import sys
import json
import pandas as pd
from dotenv import load_dotenv

# Scrapers 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Edge
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Brave
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.core.utils import ChromeType

# Email?
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_browser(browser):
    ''' Loads the appropriate driver as indicated in the .env file.

    Parameters
    ----------
    browser : str, {CHROME, EDGE, FIREFOX}
        String argument indicating the browser of preference.

    Returns
    -------
    driver : WebDriver
        Controls the Driver and allows you to drive the browser.
    '''
    
    if browser == "CHROME":
        # initialize Chrome driver
        options = webdriver.ChromeOptions()
        options.headless = True
        
        service = ChromeService(executable_path=ChromeDriverManager(path="../Drivers").install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser == "EDGE":
        # initialize MsEdge driver
        options = webdriver.EdgeOptions()
        options.headless = True

        service = EdgeService(EdgeChromiumDriverManager(path="../Drivers").install())
        driver = webdriver.Edge(service=service, options=options)

    elif browser == "FIREFOX":
        # initialize Firefox driver
        options = webdriver.FirefoxOptions()
        options.headless = True

        service = FirefoxService(GeckoDriverManager(path="../Drivers").install())
        
        driver = webdriver.Firefox(service=service, options=options)
    
    elif browser == "BRAVE":
        # initialize Brave driver
        options = webdriver.ChromeOptions()
        options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        options.headless = True
        
        service = BraveService(ChromeDriverManager(path="../Drivers", chrome_type=ChromeType.BRAVE).install())
        driver = webdriver.Chrome(service=service, options=options)

    else:
        raise ValueError("Incompatible browser! Start a GitHub issue to request this browser.")

    return driver

def load_page(f=None):
    """ Loads the unofficial transcript in Minerva using Selenium and returns the transcript_table which will be used for scraping. 
    
    Parameters
    ----------
    f : file
        Log file to be written to.

    Returns
    -------
    driver : WebDriver
        Controls the Driver and allows you to drive the browser.
        
    transcript_table : WebElement
        Object containing HTML code that describes the Minerva unofficial transcript.
    """
    
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

    # initializer driver

    browser = os.getenv("BROWSER")

    driver = load_browser(browser)
        
    # heading to Minerva login page
    URL = 'https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin'
    driver.get(URL)

    try:
    # wait for page to load
        WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.ID, "UserID")))
    except:
        if not f==None:
            f.write('Page failed to load.\n\n')
        raise ValueError('Page failed to load.')

    if login_by_ID:
        # retrieving username field and sending username
        driver.find_element(By.ID, "UserID").send_keys(sid)

        # retrieving password field and sending passowrd
        driver.find_element(By.ID, "PIN").send_keys(pin)
        
        # clicking login button
        driver.find_element(By.ID, "mcg_id_submit").click()
        
    else:
        # retrieving username field and sending username
        driver.find_element(By.ID, "mcg_un").send_keys(username)

        # retrieving password field and sending passowrd
        driver.find_element(By.ID, "mcg_pw").send_keys(password)

        # clicking login button
        driver.find_element(By.ID, "mcg_un_submit").click()

    # dealing with incorrect credentials (verifying successful login)

    # waiting for page to load --> execute_script executes JS code
    # --> waits until the JS code returns True when page is loaded
    WebDriverWait(driver=driver, timeout=10).until(
    lambda x : x.execute_script("return document.readyState === 'complete'")
    )

    try:
        errors = driver.find_element(By.NAME, "web_stop")
        f.write('Login failed.')
        raise ValueError('Login failed.')
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
    transcript_table = driver.find_elements(By.CLASS_NAME, "dedefault")

    try:
        gpa_available = driver.find_element(By.CLASS_NAME, "infotext")[1]
    except:
        gpa_available = None
    
    return driver, transcript_table, gpa_available

def minervascrape(values, term, year, transcript_table, gpa_available, terms, file):
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

    if gpa_available == None:
        gpa = 1
    elif gpa_available.text == "Credit / GPA information is not available. Please check the record again after overnight system processing has occurred.":
        gpa = 0

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
                table = transcript_table[l].find_elements(By.CLASS_NAME, "dedefault")
                for m in range(len(table)):
                    while "TERM GPA" not in table[m].text:
                        m += 1
                    term_gpa = table[m + 1].text
                    c = {"Term GPA" : term_gpa}
                    #d.append(c)
                    break
                break    
            elif "Standing" in transcript_table[j].text:
                # if gpa == 0: # return to this when gpa isn't available
                    #break
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
    ''' Converts json file to a stacked Excel file. 
    
    Parameters
    ----------
    file : str
        Filepath to json file.
        
    Returns
    -------
    df : Pandas.DataFrame
        Dataframe with multi-indexing that can be exported as Excel file.
    '''
    
    df = pd.read_json(file)

    df.set_index(['Term', 'Course Code'], inplace=True)

    return df
     
def extract_difference(old, new):
    ''' Returns a Pandas DataFrame containing the difference between the two inputs. 
    
    Parameters
    ----------
    old, new : Pandas.DataFrame
        Dataframes to be compared.
        
    Returns
    -------
    changes : Pandas.DataFrame
        DataFrame containing all transcript changes.
    '''
    
    df = old.compare(new, keep_equal=True).reset_index("Term", drop=True) # rows containing changes, Term index dropped
    
    courses = df.index.to_list()
    
    changes = new.reset_index("Term", drop=True).loc[courses, :]
    
    return changes
    
def minervaupdate(values, term, year, transcript_table, gpa_available, terms):
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
        
    changes : Pandas.DataFrame
        DataFrame containing all transcript changes.
    """
    
    with open("Updated_Scraped_Transcript.json", "w") as file:  
        minervascrape(values, term, year, transcript_table, gpa_available, terms, file)
        
    old = json2excel("Scraped_Transcript_All_Terms.json")
    new = json2excel("Updated_Scraped_Transcript.json")
        
    if old.equals(new):
        changes = None
        change = False
    else:
        if not old['Grade'].equals(new['Grade']) or not old['Course Average'].equals(new['Course Average']):
            changes = extract_difference(old, new)
            change = True
        else:
            changes = None
            change = False
            
    if change:
        # replacing old json with new json
        old_json = open("Scraped_Transcript_All_Terms.json", "w")
        new_json = open("Updated_Scraped_Transcript.json")
        
        old_json.write(new_json.read())
        
        old_json.close()
        new_json.close()
    
    os.remove("Updated_Scraped_Transcript.json")
    
    return change, changes

def generate_html(df):
    ''' Generates an HTML table based on the information from the passed Pandas DataFrame. 
    
    Parameters
    ----------
    df : Pandas.DataFrame
        Dataframe containing transcript changes.
        
    Returns
    -------
    html : str
        HTML code to be embedded in email.
    '''
    
    load_dotenv()
    name = os.getenv("NAME")
    
    html = f'''<html>
                    <head></head>
                    <body>
                        <p> Hi {name}, </p>
                        </br>
                        <p> Your transcript has updated on Minerva! View changes below: </p>
                        </br>
                        <table border="2">
                            <tr>
                                <th> Course Code </th>
                                <th> Grade </th>
                                <th> Course Average </th> 
                            </tr>'''

    table = ""

    for col, item in df.iterrows():
        table += "<tr>"
        table += "<th> " + col + " </th>"
        for i in item:
            table += "<th> " + i + " </th>"
        table += "</tr>"
        
    html += table
    html += '''</table></body></html>'''
    
    return html

def send_email(changes):
    ''' Sends the email to notify transcript changes. Attaches an HTML formatted table containing all changes. 
    
    Parameters
    ----------
    changes : Pandas.DataFrame
        DataFrame containing transcript changes to be added to HTML table.
    '''
    
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
    
    html = generate_html(changes)

    message.attach(MIMEText(html, 'html'))

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

##### ARCHIVE #####

def add_drop_remove(df):
    ''' For the sake of comparison, this function removes rows where both grade and course average are empty. We are only concerned with
    courses where the grade or course average has updated (i.e. are present). '''
    
    df = df[df['Grade'] != "Not released."] # if grade is not present, then course average is definitely not present
    
    return df
   