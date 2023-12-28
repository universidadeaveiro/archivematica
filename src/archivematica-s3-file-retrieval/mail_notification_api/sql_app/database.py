# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 28-05-2022 15:42:12
# @Description: 


import aux.constants as Constants
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser
import time
import logging
import os
import MySQLdb

# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

# Test config
try:
    # Load Variables
    Constants.DB_NAME = os.environ.get('DB_NAME', None)
    Constants.DB_LOCATION = os.environ.get('DB_LOCATION', None)
    Constants.DB_USER = os.environ.get('DB_USER', None)
    Constants.DB_PASSWORD = os.environ.get('DB_PASSWORD', None)
except:
    exit(2)

DB_OK = False
for i in range(10):
    try:
        logging.info(
            f"Trying to connect to the DB - mysql://{Constants.DB_USER}:{Constants.DB_PASSWORD}@{Constants.DB_LOCATION}/{Constants.DB_NAME}")
        SQLALCHEMY_DATABASE_URL = f"mysql://{Constants.DB_USER}:{Constants.DB_PASSWORD}@{Constants.DB_LOCATION}/{Constants.DB_NAME}"
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        DB_OK = True
        break
    except Exception as e:
        logging.error(f"Waiting for DB. Will sleep 10 more seconds... -> {e}")
        time.sleep(5)

if not DB_OK:
    logging.critical("Unable to connect to database.")
    exit(2)
