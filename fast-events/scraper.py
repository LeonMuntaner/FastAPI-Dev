import requests as _requests
import bs4 as _bs4
from typing import List

# TODO: get the url of the website
def generate_url(month: str, day: int) -> str:
    # This will take the url and return the month and day I am looking for
    url = f"https://www.onthisday.com/day/{month}/{day}"
    return url

# TODO: get the page
def get_page(url: str) -> _bs4.BeautifulSoup:
    page = _requests.get(url)
    
    # parse ther page contents in html and return the page content
    soup = _bs4.BeautifulSoup(page.content, "html.parser")
    return soup

# TODO: get events of the day
# What this function will do is return the events of a given day
def events_of_the_day(month: str, day: int) -> List[str]:
    url = generate_url(month, day)
    page = get_page(url)
    # extract the raw events from the page after inspecting the website
    raw_events = page.find_all(class_="event")
    
    # filtering and cleaning the events using list comprehension
    # this will extract the text outside of the tags
    events = [event.text for event in raw_events]
    return events

# *The scraping is pretty much done at this point. The next step is putting the contents of this in a-
# *json file. I will do this in the collect_events.py file