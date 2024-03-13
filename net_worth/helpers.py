import datetime
from dateutil.rrule import rrule, MONTHLY

def calculate_term(start: datetime.datetime, end: datetime.datetime) -> int:
    ydif = end.year - start.year
    mdif = end.month - start.month

    dif = ydif * 12 + mdif + 1

    return dif

def date_within_range(self, day: datetime.datetime, start: datetime.datetime, end: datetime.datetime):
    pass

if __name__ == "__main__":
    # TODO: add tester functions here
    pass


""" TODO: Pandas Dataframe that can extract a range fo """
# # Filter data between two dates
# filtered_df = df.loc[(df['date'] >= '2020-09-01')
#                      & (df['date'] < '2020-09-15')]