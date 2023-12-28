# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   28-05-2022 17:45:09
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 29-05-2022 15:58:36
# @Description: 

from enum import Enum
import requests
import aux.constants as Constants
from aux.mail_api_exceptions import *
import logging

# Logger
logging.basicConfig(
    format="%(module)-20s:%(levelname)-15s| %(message)s",
    level=logging.INFO
)

class EmailType(Enum):
    RETRIEVAL_REQUEST_SENT = "retrieval_request_sent"
    FILE_RETRIEVED = "file_retrieved"


class API_ENDPOINTS:
    LOGIN = "/users/login"
    NEW_EMAIL = "/email/new"
   

def send_notification_email(file_key: str, requesters: list):
    # authentication
    ret = requests.post(
        url=f'{Constants.NOTIFICATION_EMAIL_API_URL}{API_ENDPOINTS.LOGIN}',
        json={
            "username": Constants.NOTIFICATION_EMAIL_API_USERNAME,
            "password": Constants.NOTIFICATION_EMAIL_API_PASSWORD
        },
        verify=False
    )
    
    if ret.status_code != 200:
        raise AuthenticationFailed(Constants.NOTIFICATION_EMAIL_API_URL)
    
    # Get the token
    access_token = ret.json()["data"]["access_token"]
    
    # Request a new email
    ret = requests.post(
        url=f'{Constants.NOTIFICATION_EMAIL_API_URL}{API_ENDPOINTS.NEW_EMAIL}',
        json={
            "email_type": EmailType.FILE_RETRIEVED.value,
            "file_key": file_key,
            "requesters": requesters
        },
        headers={'Authorization': f'Bearer {access_token}'},
        verify=False
    )
    
    if ret.status_code != 200:
        logging.error(f"Error on Requesting Email Notification "\
            f"(status={ret.status_code}, request_text={ret.text})")
        raise CouldNotRequestEmailNotification(file_key)
