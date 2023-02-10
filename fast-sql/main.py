import fastapi as _fastapi
import services as _services
import schemas as _schemas
import sqlalchemy.orm as _orm
from typing import List

# I will use this as my decorator for when i am decorating my endpoints. 
app = _fastapi.FastAPI()

# When the code runs, the code below will make the database.db file
_services.create_database()

# TODO: create the user endpoint

@app.post("/users/", response_model=_schemas.User)
# * "user:" will be of type create, "db:" will be of type orm.Session
def create_user(user: _schemas.UserCreate, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    # I want to first check if the email that I sent is already in use 
    db_user = _services.get_user_by_email(db=db, email=user.email)
    # raise an HTTP exception if the email is already in use
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email is already in use")
    
    return _services.create_user(db=db, user=user)

# I will now create more end points for my users. This is where I will -
# make use of query parameters. 
@app.get("/users/", response_model=List[_schemas.User])
def read_users(skip: int=0, limit: int=10, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    users = _services.get_users(db=db, skip=skip, limit=limit)
    return users

# create another endpoint to return 1 user, instead of all of them
@app.get("/users/{user_id}", response_model=_schemas.User)
def read_user(user_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    db_user = _services.get_user(db=db, user_id=user_id)
    
    # what if i pass in a user id that does not exist?
    # I want to raise a 404 exception
    if db_user is None:
        raise _fastapi.HTTPException(status_code=404, detail="Sorry, this user does not exist")
    
    return db_user

# TODO: create the endpoint for the posts

@app.post("/users/{user_id}/posts/", response_model=_schemas.Post)
def create_post(user_id: int, post: _schemas.PostCreate, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    # 1st check if the user exists
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(status_code=404, detail="Sorry, this user does not exist")
    
    # 2nd return the users post 
    return _services.create_post(db=db, post=post, user_id=user_id)

# TODO: create the endpoint to get the posts
# make use of query parameters. 

@app.get("/posts/", response_model=List[_schemas.Post])
def read_posts(skip: int=0, limit: int=10, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    posts = _services.get_posts(db=db, skip=skip, limit=limit)
    return posts

# TODO: create an endpoint to read an individual post

@app.get("/posts/{post_id}", response_model=_schemas.Post)
def read_post(post_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    post = _services.get_post(db=db, post_id=post_id)
    
    if post is None:
        raise _fastapi.HTTPException(status_code=404, detail="Sorry, this post does not exist")
    
    return post

# TODO: create an endpoint that deletes posts

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    _services.delete_post(db=db, post_id=post_id)
    return {"message": f"Successfully deleted poat with id: {post_id}"}

# TODO: create an endpoint that updates the post

@app.put("/posts/{post_id}", response_model=_schemas.Post)
def update_post(post_id: int, post: _schemas.PostCreate, db: _orm.Session=_fastapi.Depends(_services.get_db)):
   return _services.update_post(db=db, post=post, post_id=post_id)