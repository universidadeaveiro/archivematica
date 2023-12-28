# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   28-05-2022 17:45:09
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 29-05-2022 15:42:05
# @Description: 

from enum import Enum
import requests
import aux.constants as Constants
from exceptions.mail_api import *


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
            "email_type": EmailType.RETRIEVAL_REQUEST_SENT.value,
            "file_key": file_key,
            "requesters": requesters
        },
        headers={'Authorization': f'Bearer {access_token}'},
        verify=False
    )

    if ret.status_code != 200:
        raise CouldNotRequestEmailNotification(file_key)
