#!/usr/bin/env python
# tickets.py - Provides tickets model for ORM.
__version__ = '0.0.1'
__author__ = 'Forest Mars'
__all__ = ['Tickets', 'drop_table']

import logging
import os
import sys

#import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine, asc, desc
from sqlalchemy import Column, and_, Date, Enum, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.sql import text
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import MetaData

from config.postgres import *


logger = logging.getLogger("tickets.py")


# DRY
try:
    engine = create_engine(SQL_URL)
    Base = declarative_base()  # ***
    Session = sessionmaker(bind=engine)
except Exception as e:
    print(e)
    sys.exit("Can't connect to database, exiting.")

# avail fields include: description, duedate, fixVersions, issuelinks, issuetype, labels, lastViewed, priority, progress, project, reporter, resolution, resolutiondate, security, status, subtasks, summary, timeestimate, timeoriginalestimate, timespent, updated, versions, votes

class Tickets(Base):
    """ Ticket model """
    __tablename__ = 'tickets'
    ticket_id = Column(Integer, primary_key=True)
    ticket_severity = Column(String)
    ticket_created_date = Column(String)
    ticket_title = Column(String)
    ticket_project = Column(String)

    def __init__(self, ticket_id, ticket_severity, ticket_created_date, ticket_title, ticket_project):
        self.ticket_id = ticket_id
        self.ticket_severity = ticket_severity
        self.ticket_created_date = ticket_created_date
        self.ticket_title = ticket_title
        self.ticket_project = ticket_project


def drop_table(table_name='tickets'):
    Base = declarative_base()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]
    if table is not None:
        Base.metadata.drop_all(engine, [table], checkfirst=True)


if __name__ == "__main__":
    if sqlalchemy.inspect(engine).has_table("tickets") is False:
        Base.metadata.create_all(engine)  # create_all is conditional but we explicitly check.
