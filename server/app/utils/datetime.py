from datetime import datetime as dt

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'

def datetime_to_string(datetime, format=DATETIME_FORMAT):
    return dt.strftime(datetime, format)

def date_to_string(datetime, format=DATETIME_FORMAT):
    return datetime_to_string(datetime, format=DATE_FORMAT)

def string_to_datetime(datetime, format=DATETIME_FORMAT):
    try:
        return dt.strptime(datetime, format)
    except:
        return dt.strptime(datetime, DATE_FORMAT)

def create_datetime():
    return dt.utcnow()