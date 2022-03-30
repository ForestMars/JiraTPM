#!/usr/bin/env python
# data_loader.py - Provides classes for SQL backend and loads generated traning set.
__version__ = '0.0.1'
__author__ = 'Forest Mars'

import base64
import json
import logging
import os
import pickle
import random
import sys
from datetime import date, datetime, timedelta  # @fixme
from datetime import datetime as dt
from pprint import pprint
from threading import Event, Thread

import numpy as np
import pandas as pd
import psycopg2
import sqlalchemy
#from sqlalchemy import create_engine, asc, desc
from sqlalchemy import Column, and_, Date, Enum, Integer, Numeric, String
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text  # SQLalchemy 1.4.32
from sqlalchemy.orm import mapper, relationship
#from protobuf_serialization import serialize_to_protobuf
#from protobuf_serialization.serialization import ProtobufDictSerializer

from config.postgres import *
from config.redis import red
# from generate_train_data import *  # or remove from run.py
from tickets import session_engine


logger = logging.getLogger("data_loader.py")
engine = session_engine()

class DBConnect():
    """ Read model connection class for handling SQL database queries. """
    def __init__(self):
        session = Session()
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        Base.query = db_session.query_property()

    def fetch(self, model: str, **kwargs):
        """ a basic sql fetcher that does not implement joins. """
        result = eval(model).query.filter_by(**kwargs)

        return result

    def fetch_first(self, model: str, **kwargs):
        """ sql fetcher for fifo queries. """
        result = eval(model).query.filter_by(**kwargs).first()

        return result

    def fetch_one(self, model: str, **kwargs):
        """ sql fetcher for singular queries. """
        result = eval(model).query.filter_by(**kwargs).one()

        return result

    def generator(self, model: str, **kwargs):
        """ generator for iterative sql querying. """
        result = eval(model).query.filter_by(**kwargs)

        for row in result:
            yield row


class QueryBuilder():
    """ Postgres write model for Jira ticket info. """

    def __init__(self) -> None:
        self.db = DBConnect()

    def schema_stream(self):
        """" Future method for decoupling db schema from data stream """
        pass

    def create_query(self, tik: dict):
        query = Tickets(
             ticket_id = tik['ticket_id'],
             ticket_severity = tik['ticket_severity'],
             ticket_created_date = tik['ticket_created_date'],
             ticket_title = tik['ticket_title'],
             ticket_project = tik['ticket_project'],
             )

        return query


class Handlers():
    def __init__(self):
        pass

    def fetch_data(self):
        """ Fetches sample Jira ticket data from generator """
        pass

    def load_pg(self):
        """ Load and transform data from Postgres backend. """
        #df = pd.read_sql("select * from \"tickets\"", engine)
        df = pd.read_sql("select ticket_created_date from \"tickets\"", engine)
        drop_cols = ['ticket_created_date', 'datetime', ]
        df['datetime'] = pd.to_datetime(df['ticket_created_date'],format='%Y-%m-%d %H:%M:%S.%f')
        df['seconds'] = df["datetime"].map(lambda ts: ts.strftime("%S"))
        df.drop(drop_cols, axis=1, inplace=True)

        return df

    def save_pg(self):
        """ Saves sample data or training dataset to Postgres backend. """
        session = Session()
        tix = get_tickets()

        for x in tix:
            session.add(query)
            session.commit()

    def save_pg_(self):
        session = Session()
        jc = JiraConnect()
        qb = QueryBuilder()

        tix = jc.get_tickets()
        for tik in tix:
            query = qb.create_query(tik)
            session.add(query)
            session.commit()


if __name__ == "__main__":
    #session_engine()
    # jira = JIRA(options, basic_auth=(user,apikey))
    pass
