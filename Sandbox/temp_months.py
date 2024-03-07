"""_summary_
"""
import datetime

from dateutil.rrule import MONTHLY, rrule


def generate_months(start: datetime.datetime, term: int) -> list:
    # payments = []
    # cur = start

    # while end > cur:
    #     payments.append(cur)
    #     cur += 
    return rrule(freq=MONTHLY, count=term, dtstart=start)

def calculate_term(start: datetime.datetime, end: datetime.datetime) -> int:
    ydif = end.year - start.year
    mdif = end.month - start.month

    dif = ydif * 12 + mdif
    print(dif)

    return dif

if __name__ == "__main__":
    START = datetime.datetime(2023, 11, 5)
    END = datetime.datetime(2033, 11, 5)
    
    TERM = calculate_term(start=START, end=END)

    print(list(generate_months(start=START, term=TERM)))
