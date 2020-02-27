# my utils module
import time


one_day = 24 * 60 * 60
one_minute = 60

def string_to_time(date_string):
    (date_s, time_s) = date_string.split(' ')
    (yyyy, MM, dd) = date_s.split('-')
    (hh, mm, ss) = time_s.split(':')
    tm = time.struct_time((int(yyyy), int(MM), int(dd), int(hh), int(mm), int(ss), 0, 0, 0))
    ts = time.mktime(tm)
    return ts