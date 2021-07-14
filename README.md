# Minervascraper

<p> Because it takes effort to log onto Minerva and navigate through the different webpages to see my grades only to realize that they haven't been uploaded yet. </p>

## Usage:
<p> Requirements: </p>
<ul>
    <li> Uses chromedriver, download the appropriate version from https://chromedriver.chromium.org/downloads and save in Minerva's parent directory </li>
</ul>
<p> .env file </p>
<ul>
    <li> Login credentials are retrieved from a .env file, stored in the same directory as the script </li>
    <li> Create a .env file following the format below
    <li> Set LOGIN=1 for ID login or LOGIN=0 for email login
</ul>

<html>
    <head>
              
        # .env

        LOGIN=1

        MCGILLID={insert ID here}
        MINERVAPIN={insert PIN here}

        MCGILLUSERNAME={insert McGill email here}
        MCGILLPASSWORD={insert password here}
        
        EMAIL={insert sender email here}
        PASS={insert sender email password here}

        MYEMAIL={insert recipient email here}
        
        NAME={Your name, so it feels a bit more personalized when email addresses you :D}

</html>

<p> To use from the command-line: </p>
<ul>
    <li> Navigate to the directory Minerva </li>
<html>
<head>
              
    cd Minerva

</html>
    <li> Run the command python minervascraper.py with no arguments to scrape for all terms </li>
<html>
<head>
              
    python minervascraper.py

</html>
    <li> Run the command python minervascraper.py ARG1 ARG2 etc... to scrape for specified terms </li>
<html>
<head>
              
    python minervascraper.py f2019 w2020 s2020 F2020

</html>
    <li> Args take the form TERM + YEAR, case-insensitive, time-independent </li>
    <ul>
        <li> TERM is represented by a single letter: </li>
        <ul>
            <li> S/s --> Summer </li>
            <li> F/f --> Fall </li>
            <li> W/w --> Winter </li>
        </ul>
        <li> YEAR has form yyyy </li>
        <li> e.g. f2019 and F2019 are equivalent for Fall term, 2019 </li>
    </ul>
    <li> Output is written to output file scraped_Transcript_TERM1_TERM2.json if terms are specified, or to scraped_Transcript_All_Terms.json if none are specified </li>
    <li> For a one-time update, use the flag -u or --update </li>
<html>
<head>
              
    python minervascraper.py -u

    python minervascraper.py --update

</html>
    <ul>
        <li> A notification is sent by email whenever an update is detected on your transcript (grade, course average) </li>
        <li> Email contains HTML formatted table that describes changes to transcript. </li>
        <li> Will not notify transcript changes relating to course add/drop </li>
    </ul>
</ul>
</p>
<p> Flags: </p>
<ul> 
    <li> -h or --help (IN PROGRESS) </li>
    <li> -u or --update </li>
</ul>

## Periodic Updates
<p> To periodically run the update on your local computer (run gradeupdate.py): </p>
<ul>
    <li> MacOS, Linux Users</li>
    <ul>
        <li> Schedule through crontab </li>
    </ul>
    <li> Windows </li>
    <ul>
        <li> Windows task scheduler </li>
    </ul>
</ul>

## To-Do:
<ul>
    <li> Make README prettier (legible) </li>
    <li> Script to create connection to task scheduler (rather than manually scheduling it (and also bc I hate the scheduler's GUI)) :/ </li>
</ul>
