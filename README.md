# MinervaScrapper

<p> Because it takes effort to log onto Minerva and navigate through the different webpages to see my grades only to realize that they haven't been uploaded yet. </p>

## Usage:
<p> Requirements: </p>
<ul>
    <li> Uses chromedriver, download the appropriate version from https://chromedriver.chromium.org/downloads </li>
</ul>
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
    </ul>
    <li> Output is written to output file Scrapped_Transcript.txt </li>
</ul>
</p>

## To-Do:
<ul>
    <li> Flags? </li>
</ul>
