import os
from dotenv import load_dotenv

# scrappers 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_page():
    
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
    """ This is the main scrapper function. Given the inputted terms (optional), the function will scrape through the user's
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
        List of Selenium.element objects that contains all the text to be parsed and scrapped.
        
    terms : dict
        Dictionary that maps the elements in term to the corresponding term name ('Fall', 'Winter', 'Summer').
        
    file : file-type
        File-type object to which the function writes.    
        
    Examples
    --------
    >> import os
    >> os.system("python minervascrapper.py f2019 w2020 S2020")
    """
    
    k = 0
    if len(values) != 0:
        file.write("Scrapped Transcript for {}\n".format(", ".join([term[i] + " " + year[i] for i in range(len(term))])))
    else:
        file.write("Scrapped Transcript for All Terms\n")
    file.write("\nTerm\tCourse Code\tGrade\tCourse Average\n")
    for i in range(len(transcript_table)):
        if len(values) != 0:
            if (term[k] not in transcript_table[i].text) or (year[k] not in transcript_table[i].text):
                continue
            else:
                file.write("\n" + term[k] + " " + year[k] + "\n")
                print("Scrapping " + term[k] + " " + year[k] + "...\n")
        else: # no arguments, scrape all terms
            if (terms['F'] not in transcript_table[i].text) and (terms['W'] not in transcript_table[i].text) and (terms['S'] not in transcript_table[i].text):
                continue
            else:
                sem = transcript_table[i].text.split()
                if len(sem) == 2:
                    file.write("\n" + sem[0] + " " + sem[1] + "\n")
                    print("Scrapping " + sem[0] + " " + sem[1] + "...\n")
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
                    file.write("Term GPA: " + term_gpa + '\n')
                    break
                break               
            course_code = transcript_table[j].text
            if "RW" in transcript_table[j - 1].text:
                file.write("\t\t" + course_code + ": Not released.\n")
            else:
                grade = transcript_table[j + 5].text
                course_avg = transcript_table[j + 9].text
                if len(course_avg.strip()) == 0:
                    file.write("\t\t" + course_code + ":\t" + grade + "\t\tNot released.\n")
                else:
                    file.write("\t\t" + course_code + ":\t" + grade + "\t\t" + course_avg + "\n")
            j += 11 # move to next course code
            if j >= len(transcript_table):
                break
        i = j
        if len(values) != 0:
            k += 1
            if k >= len(term):
                break

def minervaupdate(values, term, year, transcript_table, terms):
    """ If flagged through the command-line, this function 
    
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
        List of Selenium.element objects that contains all the text to be parsed and scrapped.
        
    terms : dict
        Dictionary that maps the elements in term to the corresponding term name ('Fall', 'Winter', 'Summer').
          
    Returns
    -------
    change : bool 
    """
    
    with open("Updated_Scrapped_Transcript.txt", "w") as file:  
        minervascrape(values, term, year, transcript_table, terms, file)
    
    os.system("diff Scrapped_Transcript_All_Terms.txt Updated_Scrapped_Transcript.txt > diff.txt")
    
    if os.path.getsize("diff.txt") != 0: # not empty file
        change = True
        # replace old file with new
        os.system("cp Updated_Scrapped_Transcript.txt Scrapped_Transcript_All_Terms.txt")
    else:
        change = False
    
    os.remove("diff.txt")
    os.remove("Updated_Scrapped_Transcript.txt")
    
    return change