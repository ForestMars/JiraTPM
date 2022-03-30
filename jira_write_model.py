    #!/usr/bin/env python
# jira_client.py - script to create random Jira tickets via Jira API
__version__ = '0.0.1'
__author__ = 'Forest Mars'
__all__ = ['JiraTickets', 'EventThread']

# import base64
import json
import logging
import os
import pickle
import random
import sys
from datetime import datetime as dt
from threading import Event, Thread

import pandas as pd
from faker import Faker
from jira import JIRA

from generate_data import get_column_data, pickle_exists


HOW_MANY = 100
HOW_LONG = 3600  # 1 hour
MAX_PER_MIN = 5
ACTIVE_PROJECT = "TES"

logger = logging.getLogger("jira_write_model.py")
user = os.environ['JIRA_USER']
server = os.environ['JIRA_URL']
apikey = os.environ['JIRA_API_KEY']  # base64 encoded
options = {'server': server}
fake = Faker()
jira = JIRA(options, basic_auth=(user,apikey))
severity_levels = ['Lowest', 'Low', 'Medium', 'High', 'Highest']


class JiraTickets():
    """ Write model for creating tickets via Jira API. """
    def __init__(self):
        self.issuetype = {'id': '10001'}
        self.ticket_titles = pickle_exists('data/summaries.pickle', get_column_data)

    def get_ticket_title(self):
        title = random.choice(self.ticket_titles) + dt.now().strftime('%M:%S.%f')[:-4]

        return title

    def get_severity(self):
        severity_name = {'name': random.choice(severity_levels)}

        return severity_name

    def create_issues(self):
        n = random.choice(list(range(MAX_PER_MIN)))
        for i in range(n):
            self.create_issue()

    def create_issue(self):
        issue_dict = {
            'project': {'key': ACTIVE_PROJECT},
            'summary': self.get_ticket_title(),
            'description': fake.text(),
            # "confluence": "link to Confluence page",
            # "verification_steps": "Verification plan",
            "priority": self.get_severity(),
            'issuetype': self.issuetype,
        }
        try:
            new_issue = jira.create_issue(fields=issue_dict)
        except Exception as e:
            logger.error(e)

class EventThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
        logger.debug("Initialized EventThread")

    def run(self):
        jtix = JiraTickets()
        ticket_count = 0
        while not self.stopped.wait(60):
            now = dt.now()
            time_diff = now - start
            if time_diff.total_seconds() > HOW_LONG:
                stopFlag.set()
            try:
                jtix.create_issues()
                ticket_count += 1
                print("created tickets")
            except Exception as e:
                logger.errror(e)


if __name__ == '__main__':
    stopFlag = Event()
    thread = EventThread(stopFlag)
    start = dt.now()
    thread.start()
