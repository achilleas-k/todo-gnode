import parsedatetime as dtparser
from datetime import datetime
from time import mktime

def parse_date(dtstring):
    stripped = dtstring.strip()
    time_struct, parse_status = dtparser.Calendar().parse(stripped)
    return datetime.fromtimestamp(mktime(time_struct)) if parse_status > 0 else ""
