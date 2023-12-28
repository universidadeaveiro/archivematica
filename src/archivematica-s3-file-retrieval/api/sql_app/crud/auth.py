# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 26-05-2022 23:40:37
# @Description: 

import logging
import random
import string
# generic imports
from os import access

from sqlalchemy.orm import Session

# custom imports
from sql_app.crud import auth as AUTH_CRUD
from sql_app.models import auth_models
#from sql_app.schemas import *
from aux import auth
from exceptions.auth import *
#from exceptions.agents import *
# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

# ---------------------------------------- #
# -----------------  Auth  --------------- #
# ---------------------------------------- #

def create_role(db: Session, role: str):
    db_role = db.query(auth_models.Role).filter(
        auth_models.Role.role == role).first()
    if not db_role:
        db_role = auth_models.Role(role=role)
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        logging.info(f"Role created : {db_role.as_dict()}")
    logging.info(f"Role {db_role.as_dict()} was already created")
    return db_role


def register_user(db: Session, username: str, password: str, roles: list) -> auth_models.User:

    # 1 - check if user already exists
    db_user = db.query(auth_models.User).filter(
        auth_models.User.username == username).first()
    if db_user:
        logging.info(f"User {username} already exists - {db_user.as_dict()}")
        return db_user
    # 2 - hash the password
    hashed_password = auth.get_password_hash(password)

    # 3 - create db checkpoint
    checkpoint = db.begin_nested()
    try:
        # 3.1 - create user
        db_user = auth_models.User(
            username=username, hashed_password=hashed_password, is_active=True)
        db.add(db_user)
        db.commit()

        # 3.2 - create user roles
        db_user_roles = []
        for role in roles:
            # get role id
            db_role = db.query(auth_models.Role).filter(
                auth_models.Role.role == role.upper()).first()
            db_user_role = auth_models.User_Role(
                user=db_user.id, role=db_role.id)
            db_user_roles.append(db_user_role)
        db.add_all(db_user_roles)
        db.commit()
        db.refresh(db_user)
    except:
        checkpoint.rollback()
        logging.info(f"Could not create user {username}")
        raise UserCreationFailed(username)
    
    logging.info(f"User {username} created with success")
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    # 1 - check if credentials are correct
    try:
        user = db.query(auth_models.User).filter(
            auth_models.User.username == username).first()
        if not auth.verify_password(password, user.hashed_password):
            raise UserInvalidCredentials(username)
    except:
        raise UserInvalidCredentials(username)
    # 2 - check if user is active
    if not user.is_active:
        raise UserNotActive(username)
    return user


def get_user_info(db: Session, username:str):
    try:
        db_user = db.query(auth_models.User).filter(
            auth_models.User.username == username).first()
    except:
        raise InvalidUser(username)
    return {
        "username": db_user.username,
        "is_active": db_user.is_active,
        "roles": get_user_roles(db, username)
    }


def get_user_roles(db: Session, username:str):
    # 1 - check if user exists
    user = db.query(auth_models.User).filter(
        auth_models.User.username == username).first()
    if not user:
        raise UserDoesNorExist(username)
    # 2 - get roles
    user_roles = db.query(auth_models.User_Role).filter(
        auth_models.User_Role.user == user.id).all()
    if len(user_roles) == 0:
        return set()
    # 3 - roles2str
    user_roles_str = []
    for user_role in user_roles:
        role = db.query(auth_models.Role).filter(
            auth_models.Role.id == user_role.role).first()
        user_roles_str.append(role.role)
    return user_roles_str
    

def update_user_password(db: Session, username: str, new_password: str):  
    try:
       # 1 - get user
        db_user = db.query(auth_models.User).filter(
            auth_models.User.username == username).first()
        # 2 - hash the password and update the db
        hashed_password = auth.get_password_hash(new_password)
        db_user.hashed_password = hashed_password
        db.commit()
        db.refresh(db_user)
    except:
        logging.info(f"Could not update {username}'s passsword")
        raise PasswordUpdateFailed(username)
    
    logging.info(f"{username}'s password updated with success")
    return db_user


def validate_if_user_is_admin(db: Session, username: str):
    user_roles = AUTH_CRUD.get_user_roles(db, username)
    
    if [True for role in user_roles if role == "ADMIN"]:
        is_admin = True
    else:
        exception = NotEnoughPrivileges()
        logging.error(exception.message)
        raise exception

    return is_admin

    
