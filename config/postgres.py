#!/usr/bin/env python
# config/postgres - Configruation for Postgres backend
__version__ = '0.0.1'
__author__ = 'Forest Mars'

import os
import json
import logging
import sys

import requests
# from sqlalchemy_utils.functions import database_exists
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

logger = logging.getLogger("__name__")

## Uncomment backend to use:
#BACKEND = 'Aurora'
#BACKEND = 'RDS'
BACKEND = 'localhost'
USE_VAULT = False

try:
    PSQL_HOST = os.environ['PSQL_HOST']
    PSQL_PORT = os.environ['PSQL_PORT'] or 5432
    PSQL_DB = os.environ['PSQL_DB']
except KeyError:
    logger.info("Check environment settings.")

if USE_VAULT == True:
    PSQL_USER, PSQL_PW = get_vault_token()
elif USE_VAULT == False:
    PSQL_USER = os.environ['PSQL_USER']
    PSQL_PW = os.environ['PSQL_PW']

SQL_URL = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    PSQL_USER,
    PSQL_PW,
    PSQL_HOST,
    PSQL_PORT,
    PSQL_DB,
    )

def session_engine():
    try:
        engine = create_engine(SQL_URL)
        Base = declarative_base()  # ***
        Session = sessionmaker(bind=engine)
        return engine
    except Exception as e:
        print(e)
        sys.exit("Can't connect to database, exiting.")


def get_vault_token():
    VAULT_HOST = os.environ['VAULT_ADDR']
    VAULT_PORT = os.environ['VAULT_PORT']
    VAULT_TOKEN = os.environ['VAULT_TOKEN']
    url = "http://{}:{}/v1/database/creds/readonly".format(VAULT_HOST, VAULT_PORT)
    headers = {'X-Vault-Token': VAULT_TOKEN}

    try:
        resp = requests.get(url, headers=headers).json()
        psql_user = resp['data']['username']
        psql_pw = resp['data']['password']
    except Exception as e:
        logger.error(e)

    return psql_user, psql_pw


if __name__ == "__main__":
    pass
