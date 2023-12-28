# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 29-05-2022 15:47:40
# @Description: 

# custom imports
import aux.constants as Constants
from sql_app.crud import auth as CRUD_Auth

# generic imports
import configparser
import logging
import os
import inspect

# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def load_config():
    # load config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Test config
    try:
        # Load Variables
        # Load Database Variables
        Constants.DB_NAME = os.environ['DB_NAME']
        Constants.DB_LOCATION = os.environ['DB_LOCATION']
        Constants.DB_USER = os.environ['DB_USER']
        Constants.DB_PASSWORD = os.environ['DB_PASSWORD']
        Constants.AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
        Constants.AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
        Constants.AWS_BUCKET_NAME = os.environ['AWS_BUCKET_NAME']
        Constants.FILE_AVAILABILITY_DAYS = int(os.environ['FILE_AVAILABILITY_DAYS'])
        Constants.NOTIFICATION_EMAIL_API_USERNAME = os.environ['NOTIFICATION_EMAIL_API_USERNAME']
        Constants.NOTIFICATION_EMAIL_API_PASSWORD = os.environ['NOTIFICATION_EMAIL_API_PASSWORD']
        Constants.NOTIFICATION_EMAIL_API_URL = os.environ['NOTIFICATION_EMAIL_API_URL']
        pass
    except Exception as e:
        logging.error(e)
        exit(1)

    return True, ""

def startup_roles(db):
    for role in Constants.USER_ROLES:
        CRUD_Auth.create_role(db, role)


def create_default_admin(db):
    CRUD_Auth.register_user(
        db = db, 
        username = Constants.DEFAULT_ADMIN_CREDENTIALS['username'], 
        password = Constants.DEFAULT_ADMIN_CREDENTIALS['password'],
        roles = Constants.USER_ROLES)
