# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 12-05-2022 15:05:22
# @Description: 

# generic imports
from typing import List
from pydantic import BaseModel
import datetime

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str
    roles: List[str]

class Token(BaseModel):
    access_token: str
    token_type: str

class NewPassword(BaseModel):
    new_password: str
