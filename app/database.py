from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/blog"

# create_engine() is a function that creates a database engine using connection url.
# connects to Database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# sessionmaker() creates a new sqlalchemy session whenever it's called.
# autocommit, autoflush disables automatic flushing and commiting.
# which means changes won't be pushed to database until you save or flush explicitly.
# session local manages database sessions during request/response cycles.
# sessions provide a way to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class provides a common base for all your declarative models
# allowing sqlalchemy to keep track of all the mapped classes in single registry.
Base = declarative_base()


# this function is called, whenever a request comes to the endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()