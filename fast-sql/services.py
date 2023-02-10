import database as _database
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas
import datetime as _dt

# TODO: create the database
def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

# TODO: create the database session
def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TODO: create a method that gets the user by email. 
# *This will take in an orm session and return the user if the email exists,
# *if it doesn't it will return none.
def get_user_by_email(db: _orm.Session, email:str):
    return db.query(_models.User).filter(_models.User.email == email).first()

# TODO: create a method that creates a user
# *This plays with the main.py create_user function 
def create_user(db: _orm.Session, user: _schemas.UserCreate):
    fake_hashed_password = user.password + "thisisnotsecure"
    db_user = _models.User(email=user.email, hashed_pass=fake_hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# TODO: create a service that gets all the users 
def get_users(db: _orm.Session, skip: int, limit: int):
    return db.query(_models.User).offset(skip).limit(limit).all()

# TODO: create a service to get individual user
def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()

# TODO: create a service for the user to create a post
def create_post(db: _orm.Session, post: _schemas.PostCreate, user_id: int):
    # I want to unpack. This will get the title and the contents
    post = _models.Post(**post.dict(), owner_id=user_id)
    
    # add the post in the database and commit it
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post

# TODO: create a service to get the users posts
def get_posts(db: _orm.Session, skip: int, limit: int):
    return db.query(_models.Post).offset(skip).limit(limit).all()

# TODO: create a dervice that returns and individual post
def get_post(db: _orm.Session, post_id: int):
    return db.query(_models.Post).filter(_models.Post.id == post_id).first()

# TODO: create a delete post service 
def delete_post(db: _orm.Session, post_id: int):
    db.query(_models.Post).filter(_models.Post.id == post_id).delete()
    db.commit()
    
# TODO: create a update post service
def update_post(db: _orm.Session, post: _schemas.PostCreate, post_id: int):
    db_post = get_post(db=db, post_id=post_id)
    db_post.title = post.title
    db_post.content = post.content
    db_post.date_last_updated = _dt.datetime.now()
    db.commit()
    db.refresh(db_post)
    
    return db_post