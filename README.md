# Minervascraper

<p> Because it takes effort to log onto Minerva and navigate through the different webpages to see my grades only to realize that they haven't been uploaded yet. </p>

## Usage:
<p> Requirements: </p>
<ul>
    <li> Uses chromedriver, download the appropriate version from https://chromedriver.chromium.org/downloads and save in Minerva's parent directory </li>
    <li> Pip install librairies python-dotenv and selenium </li>
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
    <li> Output is written to output file scraped_Transcript_TERM1_TERM2.txt if terms are specified, or to scraped_Transcript_All_Terms.txt if none are specified </li>
</ul>
</p>
<p> Flags: </p>
<ul> 
    <li> -h or --help (IN PROGRESS) </li>
    <li> -u or --update (IN PROGRESS) </li>
</ul>

## To-Do:
<ul>
    <li> Notification for when grades are released </li>
</ul>
