#!/usr/bin/env python
# run.py - Jira TPM (tickets per minute) run script
__version__ = '0.0.1'
__author__ = 'Forest Mars'

"""
    -c  create jira tickets
    -f  fetch high priority tickets and save to backend
    -b  plot bar chart tickets per minute
    -h  show this help text
"""

import argparse
import sys
from subprocess import run

from data_loader import *
from generate_data import *
from jira_read_model import *
from jira_write_model import *


DESCRIPTION = "Main execution script for Jira TPM"


def get_args(argv):
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        epilog = """ Creates sample Jira tickets and display count of high/highest severity ticket per minute. """
        )

    parser.add_argument('-c', '--create-tickets', help='create dummy jira tickets', action="store_true")
    parser.add_argument('-f', '--fetch-tickets', help='fetch high/highest priority tickets and save to daabase', action="store_true")
    parser.add_argument('-p', '--plot-data', help='plot graph of high severity tickets', action="store_true")
    parser.add_argument('-t', '--create-table', help='create tickets table for high severity Jira tickets', action="store_true")
    parser.add_argument('-d', '--drop-table', help='drop tickets table before loadng Jira tickets', action="store_true")

    return parser.parse_args(argv[1:])


class JiraTPM():
    def populate_test_database(self):
        tix = TicketData()
        tickets = tix.create_ticket_data()
        df = pd.DataFrame(tickets)
        print(df.head())

    def create_jira_tix(self, ticket_count=100):
        jc = JiraConnect()
        jira_tickets = jc.get_tickets()
        for ticket in jira_tickets:
            query = qb.create_query(ticket)
            session.add(query)
            session.commit()

    def fetch_save_tix(self):
        session_engine()  # @fixme
        session = Session()
        jc = JiraConnect()
        qb = QueryBuilder()

        if sqlalchemy.inspect(engine).has_table("tickets") is False:
            Base.metadata.create_all(engine)

        tix = jc.get_tickets()
        for tik in tix:
            query = qb.create_query(tik)
            session.add(query)
            session.commit()

    def load_from_sql(self):
        """ Loads ticket data from SQL backend. """
        handle = Handlers()
        df = handle.load_pg()
        df = df['seconds'].value_counts().sort_index()  # DRY

        return df


if __name__ == '__main__':
    tpm = JiraTPM()
    args = get_args(sys.argv)
    if args.create_tickets:
        print("\nThis script will run for 1 hour, creating a random number of Jira tickets every minute.\n")
        tpm.create_jira_tix()
    if args.fetch_tickets:
        print("\nFetching all Jira tickets with severity of High or higher and saving to database.\n")
        tpm.fetch_save_tix()
    if args.plot_data:
        print("\nLaunching dataviz dashboard on http://localhost:8050\n")
        try:
            run([sys.executable, 'app.py'])
        except Exception as e:
            logger.error(e)
    if args.create_table:
        print("\nCreating or recreating tickets table\n")
        try:
            run([sys.executable, 'tickets.py'])
            print("Tickets table successfully created")
        except Exception as e:
            logger.error(e)
    if args.drop_table:
        confirm = input("Are you sure you wish to drop the Tickets database? (This will not delete any tickets in Jira)\n")
        if confirm == 'yes':
            from tickets import drop_table
            try:
                drop_table()
                print("Tickets table successfully dropped")
            except Exception as e:
                logger.error(e)
        else:
            print("Ok, not dropping database.")
