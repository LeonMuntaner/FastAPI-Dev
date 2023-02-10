from typing import Dict
import json as _json
import datetime as _dt

# *This will be the file where I interact with the json file. I don't want to do this in my main.py-
# *file. This will keep things clean and allows me to focus on one thing only. 

# *The services file is like the middle-man between the events.json file.

# TODO: get all the events and return a dictionary
# this will be used in the main file for uploading all the data from the json file into my API.
def get_all_events() -> Dict:
    with open("events.json", encoding="utf-8") as events_file:
        data = _json.load(events_file)
    
    return data

# TODO: get the events for a specific month
# this is a simple way of doing this but it would need to be optimized later
def get_month_events(month: str) -> Dict:
    events = get_all_events()
    # this will help in case the user puts in a capital letter for the month
    month = month.lower()
    try:
        month_events = events[month]
        return month_events
    except KeyError:
        return "This month is not real"
    
# TODO: get the events for a given day
# I type casted the day in the try method because in the json file, the days are strings
def get_events_of_day(month: str, day: int) -> Dict:
    events = get_all_events()
    # this will help in case the user puts in a capital letter for the month
    month = month.lower()
    try:
        events = events[month][str(day)]
        return events
    except KeyError:
        return "No such day is available"
    
# TODO: return the events of the current day
def get_today():
    today = _dt.date.today()
    month = today.strftime("%B")
    return get_events_of_day(month, today.day)