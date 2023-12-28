# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   26-05-2022 22:09:44
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 26-05-2022 22:13:43
# @Description: 

import aux.utils as Utils
from datetime import timedelta

from fastapi import Depends, FastAPI
# generic imports
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.sql.functions import user
from sql_app.database import SessionLocal
from sqlalchemy.orm import Session
import logging
import sql_app.crud.auth as AUTH_CRUD
from aux import auth
from aux import constants as Constants
from exceptions.auth import *
import schemas.auth as AuthSchemas

# custom imports
router = APIRouter()

# Logger
logging.basicConfig(
    format="%(module)-20s:%(levelname)-15s| %(message)s",
    level=logging.INFO
)

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@router.post(
    "/users/login",
    tags=["auth"],
    summary="Login and get the authentication token",
    description="This endpoint allows the user to login and get the token."
)
def login_for_access_token(form_data: AuthSchemas.UserLogin, 
    db: Session = Depends(get_db)):
    try:
        user = AUTH_CRUD.authenticate_user(
            db, form_data.username, form_data.password)
        access_token_expires = timedelta(
            minutes=Constants.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
    except UserInvalidCredentials as e:
        return Utils.create_response(status_code=401, success=False, 
            errors=[e.message])

    return Utils.create_response(status_code=200, success=True, 
        data={"access_token": access_token, "token_type": "Bearer Token"})


@router.get(
    "/users/me/",
    tags=["auth"],
    summary="Get user information",
    description="This endpoint allows the user to get his own information."
)
def get_my_information(token: str = Depends(auth.oauth2_scheme), 
    db: Session = Depends(get_db)):
    try:
        username = auth.get_current_user(token)
        user_info = AUTH_CRUD.get_user_info(db, username)
    except Exception as e:
        return Utils.create_response(status_code=401, success=False, 
            errors=[e.message])

    return Utils.create_response(status_code=200, success=True, 
        data={"user_info": user_info})


@router.post(
    "/users/register/",
    tags=["auth"],
    summary="Register user",
    description="This endpoint allows the user to register using credentials.",
)
def register_new_user(new_user: AuthSchemas.UserRegister, 
    token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    try:
        login_username = auth.get_current_user(token)
        roles = AUTH_CRUD.get_user_roles(db, login_username)
        # check if operation was ordered by an admin
        if "ADMIN" not in roles:
            raise NotEnoughPrivileges(login_username, 'register_new_user')
        # create new user
        db_user = AUTH_CRUD.register_user(
            db, new_user.username, new_user.password, new_user.roles)
        user_info = AUTH_CRUD.get_user_info(db, db_user.username)
    except Exception as e:
        return Utils.create_response(status_code=401, success=False, 
            errors=[e.message])
    return Utils.create_response(status_code=200, success=True, 
        data={"new_user": user_info})


@router.patch(
    "/users/update-password/",
    tags=["auth"],
    summary="Update Password",
    description="This endpoint allows the user to update his password.",
)
def update_password(password_data: AuthSchemas.NewPassword, 
    token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    try:
        username = auth.get_current_user(token)
        db_user = AUTH_CRUD.update_user_password(
            db, username, password_data.new_password)
    except Exception as e:
        return Utils.create_response(status_code=403, success=False, 
            errors=[e.message])
    return Utils.create_response(status_code=200, success=True,
        message="Password Updated With Success")
