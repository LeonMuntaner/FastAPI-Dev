from fastapi import FastAPI 
import services as _services


app = FastAPI()

# TODO: create the home path/node end-point
@app.get('/')
async def Home():
    return {"Message": "Welcome to this Historical Events API"}

# TODO: create the events path end-point 
# Here i want to return all the events for the entire year.
@app.get('/events')
async def all_events():
    return _services.get_all_events()

# TODO: add dynamic endpoint where I can get the events of the current day
@app.get('/events/today')
async def events_of_today():
    return _services.get_today()

# TODO: create the monthly events path end-point
@app.get('/events/{month}')
async def events_of_the_month(month: str):
    return _services.get_month_events(month)

# TODO: create the events for a given day path end-point
@app.get('/events/{month}/{day}')
async def events_of_day(month: str, day: int):
    return _services.get_events_of_day(month, day)