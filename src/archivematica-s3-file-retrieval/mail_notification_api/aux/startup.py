# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 29-05-2022 13:30:49
# @Description: 

# custom imports
import aux.constants as Constants
from sql_app import crud

# generic imports
import logging
import os

# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

def load_config():
    try:
        # Load Variables
        Constants.NOTIFICATION_EMAIL_SMTP_SERVER = os.environ['NOTIFICATION_EMAIL_SMTP_SERVER']
        Constants.NOTIFICATION_EMAIL_SMTP_PORT = int(os.environ['NOTIFICATION_EMAIL_SMTP_PORT'])
        Constants.NOTIFICATION_EMAIL_ADDRESS = os.environ['NOTIFICATION_EMAIL_ADDRESS']
        Constants.NOTIFICATION_EMAIL_PASSWORD = os.environ['NOTIFICATION_EMAIL_PASSWORD']
        Constants.CONTACT_EMAIL = os.environ['CONTACT_EMAIL']
        Constants.FILE_AVAILABILITY_DAYS = int(os.environ['FILE_AVAILABILITY_DAYS'])
    except Exception as e:
        logging.error(e)
        exit(1)
    return True, ""


def startup_roles(db):
    for role in Constants.USER_ROLES:
        crud.create_role(db, role)


def create_default_admin(db):
    crud.register_user(
        db = db, 
        username = Constants.DEFAULT_ADMIN_CREDENTIALS['username'], 
        password = Constants.DEFAULT_ADMIN_CREDENTIALS['password'],
        roles = Constants.USER_ROLES)
