# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 28-05-2022 17:51:49
# @Description: 

# custom imports
import aux.constants as Constants

# generic imports
import logging
import os

# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

def load_config():
    # Test config
    try:
        # Load Variables
        Constants.DB_NAME = os.environ['DB_NAME']
        Constants.DB_LOCATION = os.environ['DB_LOCATION']
        Constants.DB_USER = os.environ['DB_USER']
        Constants.DB_PASSWORD = os.environ['DB_PASSWORD']
        Constants.AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
        Constants.AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
        Constants.FILE_AVAILABILITY_DAYS = int(os.environ['FILE_AVAILABILITY_DAYS'])
        Constants.POLLING_INTERVAL_HOURS = float(os.environ['POLLING_INTERVAL_HOURS'])
        Constants.NOTIFICATION_EMAIL_API_USERNAME = os.environ['NOTIFICATION_EMAIL_API_USERNAME']
        Constants.NOTIFICATION_EMAIL_API_PASSWORD = os.environ['NOTIFICATION_EMAIL_API_PASSWORD']
        Constants.NOTIFICATION_EMAIL_API_URL = os.environ['NOTIFICATION_EMAIL_API_URL']
        pass
    except Exception as e:
        logging.error(f"Error - {e}")
        exit(1)
