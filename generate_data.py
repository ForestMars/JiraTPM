#!/usr/bin/env python
# generate_training_set.py - Generate a training dataset with given formatting parameters; export to file or sql database.
__version__ = '0.0.1'
__author__ = 'Forest Mars'

import logging
import os
import pickle
import random
import sys
from pprint import pprint

import pandas as pd
from faker import Faker


ROWS = 3000


logger = logging.getLogger("generate_data.py")
fake = Faker()


def get_column_data(
            path: str = 'data/all_tickets.csv',
            col: str = 'title',
            sep: str = ',',
            ) -> list:
    """ Returns column list from specified .csv file
    Args:
        path: Path to the data file in csv format.
        col: WHich column to extract.
        sep: Separator (defaults to comma.)
    Returns:
        List of elements from specified column series.
    Raises:
        PathNotFound Exception: When no file could be found at the provided path.
    """
    if not path:
        raise FileNotFound("No path specified.")
    elif not os.path.exists(path):
        raise FileNotFound(f"No file or directory at '{path}'.")
    df = pd.read_csv(path)
    df = df.dropna()
    df.reset_index(drop=True)  # not really needed here.
    df_col = df[col].tolist()

    return df_col


# utils
def pickle_exists(path, data):
    data_ = data()

    if os.path.isfile(path):
        with open(path, "rb") as f:
            try:
                return pickle.load(f)
            except Exception:
                pass
    with open(path, "wb") as f:
        pickle.dump(data_, f)

    return data_


class TicketData():
    def __init__(self):
        self.ticket_titles = pickle_exists('var.pickle', get_data)
        self.severity_levels = ['Blocker', 'Critical', 'Major', 'Minor', 'Low']
        self.priority_levels = ['Lowest', 'Low', 'Medium', 'High', 'Highest']

    def gen_ticket_num(self, max: int=9999):
        """ Generator for training data ticket numbers. """
        num = 1
        while(num <= max):
            yield (num)
            num += 1

    def get_ticket_title(self):
        title = random.choice(self.ticket_titles)
        print(title)

        return title

    def get_assignees(self, team_size: int=20):  # @TODO: pickle this
        team = []
        for i in range(team_size):
            team.append(fake.name())

        return team

    def create_ticket_data(self):  # @TODO: Rename w/o breaking callers
        tickets = []
        tix = self.gen_ticket_num()
        assignees = self.get_assignees()
        for i in range(3000):  # @Question: use camelCase instead of snake_case here? (for transfer learning)
            tickets.append(self.get_ticket_data())

        return tickets

    def get_ticket_data(self):
        ticket_data = dict(
            tik_num = next(tix),
            tik_title = self.get_ticket_title().title(),
            tik_assignee =random.choice(assignees),
            tik_severity = random.choice(self.priority_levels),
            tik_description = fake.text()
            )
        return ticket_data

    def gen_ticket_text(self):
        tt_rows = []
        ticket_text = ['Jira ticket ', 'Jira ticket #', 'ticket ', 'ticket #']
        for i in range(ROWS):
            tt_rows.append(random.choice(ticket_text))

        return tt_rows

    def tix_over_time(self, period: int=60, total: int=100):
        n = random.choice(list(range(4)))


class Formatters():
    def __init__(self, data):
        self.df = pd.DataFrame(data)

    def target_text(self):
        """ Generate target text for semi-supervised NLG. Uses | as separator to avoid parsing difficulties. """
        df = self.df

        df = df.filter(['tik_num', 'tik_severity', 'tik_assignee'])
        df['prefix'] = 'webNLG'
        df['input_text'] = df['tik_num'].astype(str) + " | severity | " + df['tik_severity'] + " | assignee | " + df['tik_assignee']

        df_assignee = df
        df_severity = df
        df_both = df

        df_assignee['input_text'] = df['tik_num'].astype(str) + " | assignee | " + df['tik_assignee']
        df_severity['input_text'] = df['tik_num'].astype(str) + " | severity | " + df['tik_severity']
        df_both['input_text'] = df['tik_num'].astype(str) + " | severity | " + df['tik_severity'] + " | assignee | " + df['tik_assignee']

        df_assignee['target_text'] = random.choice(ticket_text) + df['tik_num'].astype(str) + " is assigned to " + df['tik_assignee']
        df_severity['target_text'] = random.choice(ticket_text) + df['tik_num'].astype(str) + " has a severity of " + df['tik_severity']
        df_both['target_text'] = random.choice(ticket_text) + df['tik_num'].astype(str) + " has a severity of " + df['tik_severity'] + " and is assigned to " + df['tik_assignee']

        df_assignee = df.drop(columns=['tik_num', 'tik_severity', 'tik_assignee'])
        df_severity = df.drop(columns=['tik_num', 'tik_severity', 'tik_assignee'])
        df_both = df.drop(columns=['tik_num', 'tik_severity', 'tik_assignee'])

        self.df_all = pd.concat([df_assignee, df_severity, df_both], axis=0)
        self.df_all.reset_index(drop=True, inplace=True)

    def to_csv(self, filepath):
        self.df_all.to_csv(filepath)


if __name__ == '__main__':
    # pd.set_option('display.max_colwidth', -1)  # @TODO: This shoould be a local environment variable.
    # cols = ,prefix,input_text,target_text

    filepath='jira-nlg-data.csv'
    tix = TicketData()
    tickets = tix.create_ticket_data()

    # Data for Jira ticket NLG model
    input("Regenerate NLG Training Set?")
    nlg_data = Formatters(tickets)
    nlg_data.target_text(tickets)
    nlg_data.to_csv()
