from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///meetme.db', echo=True)
Base = declarative_base()

########################################################################
class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password

########################################################################
class Event(Base):
    """"""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    created_by = Column(String)
    event_name = Column(String)
    event_description = Column(String)
    event_location = Column(String)
    active = Column(Boolean)

    #----------------------------------------------------------------------
    def __init__(self, created_by, event_name, event_description, event_location, active):
        """"""
        self.created_by = created_by
        self.event_name = event_name
        self.event_description = event_description
        self.event_location = event_location
        self.active = active

########################################################################
class Attendee(Base):
    """"""
    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    username = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, event_id, username):
        """"""
        self.event_id = event_id
        self.username = username

# create tables
Base.metadata.create_all(engine)
