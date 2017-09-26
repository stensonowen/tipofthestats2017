

from datetime import datetime as dt

TIMEZONE = "UTC"
FMT = "%H:%M %b %d %Y %Z" # e.g. `13:37 Sep 23 2017 UTC` # requires en locale
VALID_TIMES = [(dt.strptime(i,FMT), dt.strptime(j,FMT)) for (i,j) in [
    ("18:00 Sep 22 2017 UTC", "06:00 Sep 23 2017 UTC"), 
    ("18:00 Sep 23 2017 UTC", "06:00 Sep 24 2017 UTC"), 
    ("18:00 Sep 24 2017 UTC", "07:00 Sep 25 2017 UTC")]]    # counting the hour it ran late
    # TODO: do an hour before/after buffer or something?

def is_valid_time(datetime) -> bool:
    return any([a <= datetime < b for (a,b) in VALID_TIMES])

def timestamp_in(datetime) -> int:
    # number of minutes the event has been going
    # assumes `is_valid_time(datetime)`
    elapsed = 0
    for (a,b) in VALID_TIMES:
        if a <= datetime < b:
            # NOTE this'll fuck up if the stream lasted longer than a day
            return elapsed + (datetime-a).seconds // 60
        elapsed += (b-a).seconds // 60
    assert False #assumption was wrong


def comments_per_minute(f_in, f_out):
    f_in = open(f_in, "r")
    f_out = open(f_out, "w")
    f_out.write("Sec,\tNum,\tDatetime (utc)\n")
    daystring = None
    (last_datetime_val, last_datetime_num) = (None, 0)
    for line in f_in:
        if line.startswith("--- Log opened "):
            parts = line.split(' ')
            (month, date, year) = (parts[4], parts[5], parts[7]) # `Sep 22 2017`
            daystring = ' '.join([month, date, year])
            (last_datetime_val, last_datetime_num) = (None, 0)
        elif line.startswith("--- Day changed "):
            daystring = line[20:]
            (last_datetime_val, last_datetime_num) = (None, 0)
        else:
            clocktime = line.split(' ', 1)[0]
            timestamp = ' '.join([clocktime, daystring, TIMEZONE])
            datetime = dt.strptime(timestamp, "%H:%M %b %d %Y %Z")
            if is_valid_time(datetime) != True:
                continue
            if datetime == last_datetime_val:
                # count comments per minute
                last_datetime_num += 1
            else:
                if last_datetime_val != None:
                    event_timestamp = timestamp_in(last_datetime_val)
                    f_out.write("{:04},\t{:03},\t{}\n".format(
                        event_timestamp, last_datetime_num, last_datetime_val))
                    #NOTE this might not run the last time if the log cut off
                    # in the middle of the event (it just didn't here)
                (last_datetime_val, last_datetime_num) = (datetime, 0)

if __name__ == "__main__":
    comments_per_minute("#tipofthehats.log", "comments_per_minute.csv")




