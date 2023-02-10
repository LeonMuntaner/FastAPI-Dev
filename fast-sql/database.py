import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _dec
import sqlalchemy.orm as _orm

# *This file will be my SQLite database set up. I will use this later on with the API

# TODO: create the database url
SQLALCHEMY_DATABASE_URL = 'sqlite:///./database.db'

# TODO: create the sql engine
# The reason why I need this is because ny default SQLite only allows 1 thread to-
# communicate with it. Since i am using python and making use of python functions, i need to allow more-
# than 1 thread to interact with the database. 
engine = _sql.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# *Now that I have the engine, I can start creating the sessions

# TODO: create session 1 class
# This will be a class that i will use as a database session. It isn't a database session-
# now because I haven't created an object. But i will use it in the future to create sessions
SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

# TODO: create the base 
# This is what I will use when I create the user model and post model and it will be-
# overwritting or inherating from base.
Base = _dec.declarative_base()

# *This is all it takes to set up the SQLAlchemy! 
# *Now I will be creating my models in the models.py file