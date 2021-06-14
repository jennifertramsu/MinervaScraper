import os

def minervascrape(arguments, term, year, transcript_table, terms, file):
    """ This is the main scrapper function. Given the inputted terms (optional), the function will scrape through the user's
    unofficial transcript on Minerva and write the output (Course Code, Grade, Course Average, Term GPA) to a text file.
    
    Parameters
    ----------
    arguments : list
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
    """
    
    k = 0
    if len(arguments) != 0:
        file.write("Scrapped Transcript for {}\n".format(", ".join([term[i] + " " + year[i] for i in range(len(term))])))
    else:
        file.write("Scrapped Transcript for All Terms\n")
    file.write("\nTerm\tCourse Code\tGrade\tCourse Average\n")
    for i in range(len(transcript_table)):
        if len(arguments) != 0:
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
        if len(arguments) != 0:
            k += 1
            if k >= len(term):
                break

def minervaupdate():
    """ If flagged through the command-line, this function 
    
    Returns
    -------
    bool 
    """
    
    with open("Updated_Scrapped_Transcript.txt", "w") as file:  
        minervascrape(arguments, term, year, transcript_table, terms, file)
    
    os.system("diff Scrapped_Transcript.txt Updated_Scrapped_Transcript.txt > diff.txt")
    
    yield os.path.getsize("diff.txt") != 0 # not empty file
    
    os.remove("diff.txt")