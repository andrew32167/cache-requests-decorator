from datetime import datetime
import strict_rfc3339
import time


def utf_to_str(utf):
    '''
    Function to convert utf-8 string to python string

    :param utf: utf-8 string
    :return:
    '''
    try:
        string = unicode(utf, 'utf8')
    except TypeError:
        string = utf
    string_for_output = string.encode('utf8', 'replace')
    return string_for_output


def rfc3339_to_local(src):
    """Converts a date in RFC3339 format into a datetime in local time
    """
    ts = strict_rfc3339.rfc3339_to_timestamp(src)
    date = datetime.fromtimestamp(ts)
    return date


def local_to_rfc3339(date_to_transform):
    """
    Converts local datetime to RFC3339 format
    """
    ts = time.mktime(date_to_transform.timetuple())
    rfc = strict_rfc3339.timestamp_to_rfc3339_utcoffset(ts)
    return rfc
