# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2022-07-20 22:17:54
# @Description: 


# generic imports
from xmlrpc.client import DateTime
from MySQLdb import Timestamp
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Body
from sqlalchemy.orm import Session
from http import HTTPStatus
from typing import List
import datetime
import logging
import inspect
import boto3
import json 
import sys
import os


# custom imports
#from sql_app import crud
from sql_app.database import SessionLocal
from mail_api_wrapper import mail_api_wrapper
from schemas import s3_glacier as S3_GLACIER_SCHEMAS
from aux.file_to_retrieve_status import FileToRetrieveStatusEnum
from sql_app.crud import s3_glacier as S3_GLACIER_CRUD
from sql_app.crud import auth as AUTH_CRUD
from schemas import auth as AUTH_SCHEMAS
from aux import auth
from exceptions.auth import *
import aux.constants as Constants
import aux.utils as Utils
from functools import wraps


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
        

def rbac_enforcer(role):
    def inner(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token = kwargs.get('token')
            db = kwargs.get('db')
            try:
                username = auth.get_current_user(token)
                roles = AUTH_CRUD.get_user_roles(db, username)
                if role not in roles:
                    raise Exception
            except:
                return Utils.create_response(status_code=400, success=False,
                    errors=[f"Insufficient permissions to access this resource. " +
                            "This is resource is only available to users with " +
                            f"the role: '{role}'"]
                    )
            return await func(*args, **kwargs)
        return wrapper
    return inner


@router.post(
    "/files/retrieve",
    tags=["s3_glacier"],
    summary="Retrieve a file from S3 Glacier",
    description="Retrieve a file from S3 Glacier",
)
@rbac_enforcer("ADMIN")
async def retrieve_file(new_file_retrieval: S3_GLACIER_SCHEMAS.NewFileRetrieval,
    token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    try:
        file_to_retrieve = S3_GLACIER_CRUD.get_file_to_retrieve(
            db, 
            file_to_retrieve_key = new_file_retrieval.file_key
        )

        # if file doesn't exist in the database, create it and create a 
        # retrieval order
        if not file_to_retrieve:
            # Create new file to retrieve
            file_to_retrieve = S3_GLACIER_CRUD.create_file_to_retrieve(
                db, 
                new_file_retrieval.bucket_name, 
                new_file_retrieval.file_key
            )
            # Create new file to request
            S3_GLACIER_CRUD.create_file_to_retrieve_request(
                db, 
                file_to_retrieve.id, 
                new_file_retrieval.requesters_email
            )

        last_retrieved_timestamp = file_to_retrieve.last_retrieved_timestamp \
            if file_to_retrieve.last_retrieved_timestamp \
            else datetime.datetime.now() - \
            datetime.timedelta(days=Constants.FILE_AVAILABILITY_DAYS + 1)
        
        last_retrieval_request_time = file_to_retrieve.last_retrieval_request_time \
            if file_to_retrieve.last_retrieval_request_time \
            else datetime.datetime.now() - \
            datetime.timedelta(days=Constants.FILE_AVAILABILITY_DAYS + 1)
        
        # If the file was retrieved in the last 7 days, just return OK  
        if last_retrieved_timestamp > datetime.datetime.now() - \
            datetime.timedelta(days=Constants.FILE_AVAILABILITY_DAYS ):
            
            # Send email
            mail_api_wrapper.send_notification_email(
                new_file_retrieval.file_key,
                [new_file_retrieval.requesters_email]
            )
            return Utils.create_response(
                data=file_to_retrieve.as_dict(), 
                message="File should be available"
            )
        
        # else, we need to check if it already being retrieved or not
        # if it is being retrieved
        if last_retrieval_request_time > datetime.datetime.now() - \
            datetime.timedelta(days=Constants.FILE_AVAILABILITY_DAYS):
                
            S3_GLACIER_CRUD.create_file_to_retrieve_request(
                db, 
                file_to_retrieve.id,
                new_file_retrieval.requesters_email
            )
            
            # Send email
            mail_api_wrapper.send_notification_email(
                new_file_retrieval.file_key, 
                [new_file_retrieval.requesters_email]
            )
        
            return Utils.create_response(
                data=file_to_retrieve.as_dict(), 
                message="File is already being retrieved"
            )

        # else, retrieve the file
        
        s3 = boto3.resource(
            's3', 
            aws_access_key_id=Constants.AWS_ACCESS_KEY_ID, 
            aws_secret_access_key=Constants.AWS_SECRET_ACCESS_KEY
        )
        bucket = s3.Bucket(Constants.AWS_BUCKET_NAME)

        r = bucket.meta.client.restore_object(
            Bucket=new_file_retrieval.bucket_name,
            Key=new_file_retrieval.file_key,
            RestoreRequest={
                'Days': Constants.FILE_AVAILABILITY_DAYS,
                'GlacierJobParameters': {
                    'Tier': 'Standard'
                }
            }
        )

        file_to_retrieve = S3_GLACIER_CRUD.update_file_to_retrieve(
            db, 
            file_to_retrieve.id, 
            datetime.datetime.now()
        ) 
        
        S3_GLACIER_CRUD.update_file_to_retrieve_status(
            db,
            file_to_retrieve.id,
            FileToRetrieveStatusEnum.GLACIER_RETRIEVAL_REQUESTED
        )
        
        # Send email
        mail_api_wrapper.send_notification_email(
            new_file_retrieval.file_key, 
            [new_file_retrieval.requesters_email]
        )
        
        return Utils.create_response(
            data=file_to_retrieve.as_dict(),
            message="A file retrieval request was made"
        )
    
    except Exception as e:
        logging.error(e)
        return Utils.create_response(status_code=400, success=False,
            errors=[f"Error - {e}."])


@router.get(
    "/files/retrieval-status/{file_id}",
    tags=["s3_glacier"],
    summary="Verify the status of a file retrieval",
    description="Verify the status of a file retrieval",
)
async def retrieval_status(file_id = int,  db: Session = Depends(get_db)):
    try:
        # Retrieve file status
        file_to_retrieve_status = S3_GLACIER_CRUD.get_file_to_retrieve_status(db, file_id)
        file_to_retrieve_status_dict = [s.as_dict() for s in file_to_retrieve_status]

        return Utils.create_response(data=file_to_retrieve_status_dict,
            message="The file status was successfully retrieved")
    except Exception as e:
        logging.error(f"Error - {e}")
        return Utils.create_response(status_code=400, success=False, 
            errors=[f"Error - {e}."])


@router.get(
    "/files/retrieval-info/{file_id}",
    tags=["s3_glacier"],
    summary="",
    description="",
)
@rbac_enforcer("ADMIN")
async def retrieval_info(file_id: int, token: str = Depends(auth.oauth2_scheme),
    db: Session = Depends(get_db)):
    try:
        # Get file data
        file_info = S3_GLACIER_CRUD.get_file_to_retrieve(db, file_id).as_dict()
         
        # Get file requests status
        file_to_retrieve_status = S3_GLACIER_CRUD.get_file_to_retrieve_status(db, file_id)
        file_to_retrieve_status_dict = [s.as_dict() for s in file_to_retrieve_status]
        
        # Get file requesters
        file_to_retrieve_requests = S3_GLACIER_CRUD.get_file_to_retrieve_requests(db, file_id)
        file_to_retrieve_requests_dict = [r.as_dict() for r in file_to_retrieve_requests]

        # Gather both status and requesters 
        file_to_retrieve_info = {
            "file": file_info,
            'requesters': file_to_retrieve_requests_dict,
            'status': file_to_retrieve_status_dict
        }
                
        return Utils.create_response(data = file_to_retrieve_info)
    except Exception as e:
        logging.error(f"Error - {e}")
        return Utils.create_response(status_code=400, success=False,
            errors=[f"Error - {e}."])


@router.get(
    "/files/",
    tags=["s3_glacier"],
    summary="",
    description="",
)
@rbac_enforcer("ADMIN")
async def get_all_files(token: str = Depends(auth.oauth2_scheme),  
    db: Session = Depends(get_db)):
    try:
        # Get all Files To Retrieve
        files_to_retrieve = S3_GLACIER_CRUD.get_all_files_to_retrieve(db)
        files_to_retrieve_dict = [f.as_dict() for f in files_to_retrieve]

        return Utils.create_response(data = files_to_retrieve_dict)
    except Exception as e:
        logging.error(f"Error - {e}")
        return Utils.create_response(status_code=400, success=False, 
            errors=[f"Error - {e}."])


@router.get(
    "/files/file/{file_id}",
    tags=["s3_glacier"],
    summary="",
    description="",
)
@rbac_enforcer("ADMIN")
async def get_file_info(file_id: int, token: str = Depends(auth.oauth2_scheme),
    db: Session = Depends(get_db)):
    try:
        # Get file info
        file_info = S3_GLACIER_CRUD.get_file_to_retrieve(db, file_id).as_dict()

        return Utils.create_response(data=file_info)
    except Exception as e:
        logging.error(f"Error - {e}")
        return Utils.create_response(status_code=400, success=False, 
            errors=[f"Error - {e}."])



@router.get(
    "/files/requesters",
    tags=["s3_glacier"],
    summary="",
    description="",
)
@rbac_enforcer("ADMIN")
async def get_all_requesters(token: str = Depends(auth.oauth2_scheme), 
    db: Session = Depends(get_db)):
    try:
        # Get list of all file retrieve requests
        requests = S3_GLACIER_CRUD.get_file_to_retrieve_requests(db)
       
        requesters = dict()

        for request in requests:
            if request.requesters_email not in requesters:
                requesters[request.requesters_email] = [request.file_id]
            else:
                if request.file_id not in requesters[request.requesters_email]:
                    requesters[request.requesters_email].append(request.file_id)

        return Utils.create_response(data = requesters)
    except Exception as e:
        logging.error(f"Error - {e}")
        return Utils.create_response(status_code=400, success=False, 
            errors=[f"Error - {e}."])


## Push Events
@router.post(
    "/files/s3-notifications",
    tags=["s3_glacier"],
    summary="Receives AWS S3 Glacier notifications",
    description="Receives AWS S3 Glacier notifications",
)
#@rbac_enforcer("ADMIN")
async def s3_notifications(payload: dict = Body(...)):
    try:
        data = payload
        print(data)
        return  Utils.create_response(
            data=dict(data),
            message="Received AWS S3 Glacier notifications"
        )
    except Exception as e:
        logging.error(e)
        return Utils.create_response(status_code=400, success=False,
            errors=[f"Error - {e}."])

