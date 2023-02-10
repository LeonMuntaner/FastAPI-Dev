import pydantic as _pydan
import datetime as _dt
from typing import List

# *I will be creating the serializers. This will basically shpae the model or the data which the-
# *API will recieve and respond with. 

# *I want to layout what our responses and requests will look like.

# TODO: create the post base
# i will use this to inheret from later on 
# I will only be declaring data types here
class _PostBase(_pydan.BaseModel):
    title: str
    content: str

# TODO: create the post create
# This will be the data shape I want when creating a post.
# I want it to inheret from PostBase

# When creating a post I will only be sending the title and the content.
class PostCreate(_PostBase):
    pass 

# TODO: create the post in general
# this is what I will use to read a post.
# this will of course have everything else like the id, title content, ect..
class Post(_PostBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime
    
    # TODO: create the config inside the Post class
    # *The reason i am doing this is because by default the orm mode is set to false.
    # *I want this to be True because when I load the user, I want the post to come with it.
    # *By default SQLAlchemy does lazy-loading and I don't want lazy loading here.
    # *I want to show the posts as well. 
    class Config:
        orm_mode = True

# TODO: create the user base class and inheret from pydantic base
class _UserBase(_pydan.BaseModel):
    email: str
    
# TODO: create the User create class
class UserCreate(_UserBase):
    password: str
    
# TODO: create User class
class User(_UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []
    
    class Config:
        orm_mode = True