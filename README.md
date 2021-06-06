# MinervaScrapper

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
    <li> Run the command python minervascrapper.py ARG1 ARG2 etc... </li>
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
    <li> Output is written to output file Scrapped_Transcript.txt </li>
</ul>
</p>

## To-Do:
<ul>
    <li> Flags? </li>
    <li> Notification for when grades are released </li>
</ul>
