
# format:
#   (minutes event has been live, number of comments in this minute)

from datetime import datetime as dt

TIMEZONE = "UTC"
FMT = "%H:%M %b %d %Y %Z"
VALID_TIMES = [("18:00 Sep 22 2017 UTC", "06:00 Sep 23 2017 UTC"), 
        ("18:00 Sep 23 2017 UTC", "06:00 Sep 24 2017 UTC"), 
        ("18:00 Sep 24 2017 UTC", "07:00 Sep 25 2017 UTC")]
VALID_TIMES = [(dt.strptime(i,FMT), dt.strptime(j,FMT)) for (i,j) in VALID_TIMES]

def is_valid_time(datetime) -> bool:
    return any([a <= datetime <= b for (a,b) in VALID_TIMES])

def comments_per_minute(f_in, f_out):
    f_in = open(f_in, "r")
    f_out = open(f_out, "w")
    switch_day_0 = ""
    switch_day_1 = ""
    switch_day_2 = ""
    daystring = None
    for line in f_in:
        # start at 19:00 
        if line.startswith("--- Log opened "):
            parts = line.split(' ')
            month = parts[4] # Sep
            date = parts[5]  # 22
            year = parts[7]  # 2017
            daystring = ' '.join([month, date, year])
        elif line.startswith("--- Day changed "):
            daystring = line[20:]
        else:
            clocktime = line.split(' ', 1)[0]
            timestamp = ' '.join([clocktime, daystring, TIMEZONE])
            # e.g. `13:37 Sep 23 2017 UTC`
            datetime = dt.strptime(timestamp, "%H:%M %b %d %Y %Z")
            print(datetime)
            break


if __name__ == "__main__":
    comments_per_minute("#tipofthehats.log", "output")




