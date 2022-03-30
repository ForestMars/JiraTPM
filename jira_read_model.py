    #!/usr/bin/env python
# jira_featch.py - non-compiiled version of jira_info demo. Requires Jira API key and running Postgres backend.
__version__ = '0.0.1'
__author__ = 'Forest Mars'
__all__ = ['JiraConnect']

import base64
import json
import logging
import os
import pickle
import random
import sys
from datetime import date, datetime, timedelta  # @fixme
from datetime import datetime as dt
from decimal import Decimal
from pprint import pprint
from threading import Event, Thread

import numpy as np
import pandas as pd
import psycopg2
import sqlalchemy
from faker import Faker
from jira import JIRA
from sqlalchemy import create_engine, asc, desc
from sqlalchemy import Column, and_, Date, Enum, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text  # SQLalchemy 1.4.32
from sqlalchemy.orm import mapper, relationship
#from protobuf_serialization import serialize_to_protobuf
#from protobuf_serialization.serialization import ProtobufDictSerializer

from config.postgres import *
from config.redis import red

logger = logging.getLogger("run.py")


ACTIVE_PROJECT = "TES"

user = os.environ['JIRA_USER']
server = os.environ['JIRA_URL']
apikey = os.environ['JIRA_API_KEY']  # base64 encoded
options = {'server': server}

jira = JIRA(options, basic_auth=(user,apikey) )


class JiraConnect():
    """ Format queries for Jira API """
    def __init__(self):
        self.jql_query = "priority IN ('High', 'Highest') order by created asc"

    def get_tickets(self):
        tickets = []

        for issue in jira.search_issues(self.jql_query, maxResults=0):
            ticket = dict(
                ticket_id = issue.id,
                ticket_severity = issue.fields.priority.name,
                ticket_created_date = issue.fields.created,
                ticket_title = issue.fields.summary,
                ticket_project = ACTIVE_PROJECT,
                )
            tickets.append(ticket)

        for ticket in tickets:
            yield ticket


if __name__ == "__main__":
    tix = jc.get_tickets()
    for tik in tix:
        query = qb.create_query(tik)
        session.add(query)
        session.commit()
