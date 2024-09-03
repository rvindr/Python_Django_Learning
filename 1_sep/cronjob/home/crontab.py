# home/crontab.py

import datetime

def my_scheduled_job():
    with open("/Users/ravinderverma/Learning/janbask/1_sep/cronjob/cronjob_log.txt", "a") as log_file:
        log_file.write(f"Job ran at {datetime.datetime.now()}\n")
