from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None

Base = declarative_base()

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///user_reports.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()


# ENGINE = None
# Session = sessionmaker(bind=ENGINE)
# ENGINE = create_engine("sqlite:///user-reports.db", echo=False)


# Base.query = session.query_property()

### Class declarations go here

class Status(Base):
    __tablename__       = "statuses"
    id                  = Column(Integer,       primary_key = True)
    venue_name          = Column(String,        nullable    = True)
    foursquare_id       = Column(String,        nullable    = False)
    status              = Column(Integer,       nullable    = False)
    time                = Column(DateTime,      nullable    = False)
    expiration_status   = Column(String,        nullable    = False)

 
def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()