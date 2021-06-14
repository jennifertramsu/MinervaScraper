# auth things
import sys
from crontab import CronTab

## idea:
# --> use crontab to enable and disable the script to run on a schedule
# --> customizable?
# --> every time the script is run, the new file is compared to an existing scrapped file
# --> if diff returns nothing, no change
# --> otherwise, an update is present, send to email
# --> ideally, Linux's crontab has an option to send email, idk about Python ?-?