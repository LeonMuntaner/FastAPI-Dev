import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import database as _db
import datetime as _dt
# *If you are familiar with flask or django this is basically where we define our tables.
# *This is how we would want our sql tables to look inside the database.

# *One thing to point out is that the word 'model' takes different forms when using pydantic.
# *FAST API makes use of pydantic, which is like a type-system for python but stronger.
# *Then the word model means something else.

# *I will be creating 2 tables. The user table and the post table. I will also be using-
# *the Base from the database.py file. As I will use the Base when i inheret when creating-
# *the user and post models.

# TODO: create the User table
class User(_db.Base):
    __tablename__ = 'users'
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    
    # creating a hashed password as I don't want to store the passwords in plane text
    hashed_pass = _sql.Column(_sql.String)
    
    # this will tell whether the user is active or not
    # when a user is created by default is_active will be set to true 
    is_active = _sql.Column(_sql.Boolean, default=True)
    
    # this will be the post the user has
    # 'Post' will be the name of my model
    posts = _orm.relationship('Post', back_populates='owner')
    
# TODO: create the post table
class Post(_db.Base):
    __tablename__ = 'posts'
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    
    # contemts the user posts 
    content = _sql.Column(_sql.String, index=True)
    
    # which user created the post
    # The reason i set the foreign key as users and not user is because i have set the-
    # table name as users and it will look for that and not User
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey('users.id'))
    
    # setting the date created for a post
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    
    # since I will be updating the posts, it would be nice to have this update info 
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    
    owner = _orm.relationship('User', back_populates='posts')

# *Basically when we look up a user, as we will see in the API, we will also see when fetching a user for example,-
# *we will see the posts they have created. 

# *Next I will be creating the schemas that FAST API will be using as validation for the data its getting and recieving.