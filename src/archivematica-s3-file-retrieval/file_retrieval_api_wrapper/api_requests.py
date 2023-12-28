# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   30-05-2022 22:00:38
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 30-05-2022 22:08:15
# @Description: 

import requests
import logging

# Disable SSl warnings
requests.packages.urllib3.disable_warnings()

# Logger
logging.basicConfig(
    format="%(module)-25s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)


class MailAPIRequests:

    token = None
    expire_time = None

    def __init__(self, host: str, username: str, password: str):
        
        self.host = host
        self.username = username
        self.password = password


    def requires_auth(func, *args, **kwargs):
        def wrapper(self, *args, **kwargs):
            if not self._is_authenticated():
                logging.info("Token has expired. Authenticating again...")
                self._authenticate()
            return func(self, *args, **kwargs)
        return wrapper


    def _is_authenticated(self) -> bool:
        r = requests.get(
            url=f'{self.host}/users/me',
            headers={'Authorization': f'Bearer {self.token}'},
            verify=False
        )
        return r.status_code == 200

    
    def _authenticate(self) -> bool:
        obj = {
            "username": self.username,
            "password": self.password
        }

        r = requests.post(
            url=f'{self.host}/users/login',
            json=obj,
            verify=False
        )
        
        if r.status_code == 200:
            logging.info("Authentication Successful")
            self.token = r.json()["data"]["access_token"]
            return True
        return False
    
    
    @requires_auth
    def retrieve_file(self, bucket, file_key, requester):
        
        obj = {
            "file_key": file_key,
            "bucket_name": bucket,
            "requesters_email": requester
        }
        
        ret = requests.post(
            url=f'{self.host}/files/retrieve',
            headers={'Authorization': f'Bearer {self.token}'},
            json=obj,
            verify=False
        )
        # check if the response is valid
        if ret.status_code != 200:
            raise Exception("Unable to request file retrieval")
