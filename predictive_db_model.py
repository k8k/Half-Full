from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session


ENGINE = None
Session = None

Base = declarative_base()

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///checkins_venues.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()


# ENGINE = None
# Session = sessionmaker(bind=ENGINE)
# ENGINE = create_engine("sqlite:///user-reports.db", echo=False)

# Base.query = session.query_property()



class Status(Base):
    __tablename__       = "statuses"
    id                  = Column(Integer,       primary_key = True)
    venue_name          = Column(String,        nullable    = True)
    foursquare_id       = Column(String,        nullable    = False)
    status              = Column(Integer,       nullable    = False)
    time                = Column(DateTime,      nullable    = False)
    expiration_status   = Column(String,        nullable    = False)

class Venue(Base):
    __tablename__       = "venues"
    id                  = Column(Integer,       primary_key = True)
    venue_name          = Column(String,        nullable    = True)
    foursquare_id       = Column(String,        nullable    = False)
    category            = Column(String,        nullable    = True)
    latitude            = Column(Integer,       nullable    = False)
    longitude           = Column(Integer,       nullable    = False)

class Checkin(Base):
    __tablename__       = "checkins"
    id                  = Column(Integer,       primary_key = True)
    venue_name          = Column(String,        nullable    = True)
    foursquare_id       = Column(String,        nullable    = False)
    current_checkins    = Column(Integer,       nullable    = False)
    checkin_time        = Column(DateTime,      nullable    = False)


def main():
    pass

if __name__ == "__main__":
    main()