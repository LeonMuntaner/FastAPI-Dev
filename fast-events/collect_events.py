import datetime as _dt
from typing import Iterator, Dict
import scraper as _scraper
import json as _json

# *I want to collect the data from january to the end of the year. The way that I will do this-
# *is by creating a function that allows me to loop through every day of the year, and also-
# *keeps in mind that there are leap years.

# TODO: create the date range function
# This function returns an iterater
def date_range(start_date: _dt.date, end_date: _dt.date) -> Iterator[_dt.date]:
    # Now i will create the for loop from the start of the year, till the end.
    # convert the difference into integer values
    for n in range(int((end_date - start_date).days)):
        # I want to yield each day afterwards from the start date.
        # use timedelta so that i can increment the time
        yield start_date + _dt.timedelta(n)
        
# TODO: get the desired events and put them in a dictionary
def create_events_dict() -> Dict:
    events = dict()
    
    # start date will be january first
    start_date = _dt.date(2020, 1, 1)
    
    # end date will be january 2021
    end_date = _dt.date(2021, 1, 1)
    
    for date in date_range(start_date, end_date):
        # since in the scaper.py file i'm getting the month as a string-
        # i need to convert it into strftime
        month = date.strftime('%B').lower()
        if month not in events:
            events[month] = dict()
        
        events[month][date.day] = _scraper.events_of_the_day(month, date.day)
    
    return events

# TODO: add all of the information into a json file 
# putting this here so that if anyone runs this, it will update the json
if __name__ == "__main__":
    events = create_events_dict()
    with open("events.json", mode="w", encoding="utf-8") as events_file:
        # dump into json
        _json.dump(events, events_file, ensure_ascii=False)