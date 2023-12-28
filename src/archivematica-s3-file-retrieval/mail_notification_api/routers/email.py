# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 29-05-2022 13:08:18
# @Description: 


# generic imports
from xmlrpc.client import DateTime
from MySQLdb import Timestamp
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
import smtplib
import certifi
import ssl
import logging


# custom imports
#from sql_app import crud
from sql_app.database import SessionLocal
from aux.smtp import SMTPWrapper
from sql_app import crud
from aux import auth
import aux.constants as Constants
import aux.utils as Utils
from functools import wraps
from aux import email
import schemas


# start the router
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


# SMTP Server
SMTP_SESSION = None
     

def rbac_enforcer(role):
    def inner(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token = kwargs.get('token')
            db = kwargs.get('db')
            try:
                username = auth.get_current_user(token)
                roles = crud.get_user_roles(db, username)
                logging.info(roles)
                if role not in roles:
                    raise Exception
            except Exception as e:
                return Utils.create_response(status_code=400, success=False,
                    errors=[f"Insufficient permissions to access this resource. " +
                            "This is resource is only available to users with " +
                            f"the role: '{role}', {e}"]
                    )
            return await func(*args, **kwargs)
        return wrapper
    return inner


@router.post(
    "/email/new",
    tags=["email"],
    summary="Send a New Notification E-mail",
    description="Send a New Notification E-mail",
)
@rbac_enforcer("ADMIN")
async def retrieval_info(request: schemas.NewEmail,
    token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    global SMTP_SESSION
    try:
        # get smtp wrapper
        if not SMTP_SESSION: SMTP_SESSION = SMTPWrapper()
        # compose the email message and send it
        email_obj = email.Email(request.email_type, request.file_key)

        SMTP_SESSION.send_email(
            Constants.NOTIFICATION_EMAIL_ADDRESS,
            request.requesters,
            email_obj.compose_email()
        )                 
        return Utils.create_response(message="Emails sent successfully!")
    except Exception as e:
        logging.error(f"Error - {e}")
        return Utils.create_response(status_code=400, success=False,
            errors=[f"Error - {e}."])
