# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 28-05-2022 18:43:43
# @Description: 

import datetime
import logging
from asyncore import file_dispatcher
# generic imports
from os import access


from aux.s3_exceptions import *
from aux.file_to_retrieve_status import FileToRetrieveStatusEnum
# custom imports
from sql_app import models
from sqlalchemy.orm import Session
from sqlalchemy import or_


# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

# ---------------------------------------- #
# --------------  S3 Glacier  ------------ #
# ---------------------------------------- #


def get_file_to_retrieve(
        db: Session,
        file_to_retrieve_id: int = None,
        file_to_retrieve_key: str = None
    ) -> models.FileToRetrieve:
    """CRUD Operation to Get a File To Retrieve from the database

    Args:
        db (Session): database session
        file_to_retrieve_id (int): file to retrieve id in the database

    Raises:
        exception: FileToRetrieveDoesNotExist

    Returns:
        models.File_To_Retrieve: file to retrieve
    """
    # Get the file to retrieve
    if file_to_retrieve_id:
        return db.query(models.FileToRetrieve).filter(
        models.FileToRetrieve.id == file_to_retrieve_id).first()
    if file_to_retrieve_key:
        return db.query(models.FileToRetrieve).filter(
        models.FileToRetrieve.file_key == file_to_retrieve_key).first()


def create_file_to_retrieve(
        db: Session,
        bucket_name: str,
        file_key: str
    ) -> models.FileToRetrieve:
    """ CRUD Operation to Create a new File To Retrieve

    Args:
        db (Session): database session
        bucket_name (str): s3 bucket name
        file_key (str): file unique key in s3

    Returns:
        models.File_To_Retrieve: new file to retrieve
    """
    # Check if this file was already created
    db_file_to_retrieve = db.query(models.FileToRetrieve).filter(
        models.FileToRetrieve.bucket_name == bucket_name, 
        models.FileToRetrieve.file_key == file_key
        ).first()
    if not db_file_to_retrieve:
        db_file_to_retrieve = models.FileToRetrieve(
            bucket_name=bucket_name,
            file_key=file_key,
        )
        db.add(db_file_to_retrieve)
        db.commit()
        db.refresh(db_file_to_retrieve)
        logging.info(f"File To Retrieve Created: {db_file_to_retrieve.as_dict()}")
        
        # Create a new File to Retrieve Status
        db_file_to_retrieve_status = models.FileToRetrieveStatus(
            file_id=db_file_to_retrieve.id,
            status=FileToRetrieveStatusEnum.FILE_ADDED_TO_DATABASE.value
        )
        db.add(db_file_to_retrieve_status)
        db.commit()
    logging.info(f"File To Retrieve {db_file_to_retrieve.as_dict()}" \
        "was already created.")
    return db_file_to_retrieve


def update_file_to_retrieve(
        db: Session,
        file_to_retrieve_id: int,
        last_retrieval_request_time: datetime.datetime = None,
        last_retrieved_timestamp: datetime.datetime = None,
        timestamp_of_file_removal: datetime.datetime = None,
    ) -> models.FileToRetrieve:
    """CRUD Operation to Update a File To Retrieve

    Args:
        db (Session): database session
        file_to_retrieve_id (int): file to retrieve id in the database
        last_retrieval_request_time (datetime.datetime, optional): \
            Timestamp of the last retrieval request. Defaults to None.
        last_retrieved_timestamp (datetime.datetime, optional): \
            Timestamp of the last time the file was retrieved. Defaults to None.
        timestamp_of_file_removal (datetime.datetime, optional): \
            Timestamp relative to the removal of the file from the direct \
                access layer. Defaults to None.
    Returns:
        models.File_To_Retrieve: updated file to retrieve
    """
    # Get the file to retrieve
    db_file_to_retrieve = get_file_to_retrieve(db, file_to_retrieve_id)
    
    # Else, check the fields to be updated
    if last_retrieval_request_time:
        db_file_to_retrieve.last_retrieval_request_time = last_retrieval_request_time
    if last_retrieved_timestamp:
        db_file_to_retrieve.last_retrieved_timestamp = last_retrieved_timestamp
    if timestamp_of_file_removal:
        db_file_to_retrieve.timestamp_of_file_removal = timestamp_of_file_removal
    
    # Update it in the database and refresh the object instance
    db.commit()
    db.refresh(db_file_to_retrieve)
    logging.info(f"File To Retrieve was updated: {db_file_to_retrieve.as_dict()}.")
    return db_file_to_retrieve


def create_file_to_retrieve_request(
    db: Session, 
    file_to_retrieve_id: int, 
    requesters_email: str
    ) -> models.FileToRetrieveRequest:
    """CRUD Operation to Create a new File To Retrieve Request in the database

    Args:
        db (Session): database session
        file_to_retrieve_id (int): file to retrieve id in the database
        requesters_email (str): email of the requester

    Returns:
        models.FileToRetrieveRequest: new file to retrieve request
    """
    # Check if a file to retrieve entry exists in the database
    # If it doesn't exist, raise an exception
    get_file_to_retrieve(db, file_to_retrieve_id)
    
    # Create a File to Retrieve Request
    db_file_to_retrieve_request = models.FileToRetrieveRequest(
        file_id=file_to_retrieve_id,
        requesters_email=requesters_email,
    )
    db.add(db_file_to_retrieve_request)
    db.commit()
    db.refresh(db_file_to_retrieve_request)
    logging.info(
        f"File To Retrieve Request Created: {db_file_to_retrieve_request.as_dict()}")
    
    return db_file_to_retrieve_request


def get_file_to_retrieve_requests(
    db: Session,
    file_id: int = None
    ) -> models.FileToRetrieveRequest:
    """CRUD Operation to Get all requesters e-mails, and the files they requested or all

    Args:
        db (Session): database session

    Returns:
        file_to_retrieve_requests: list containing file to retrieve requests
    """
    if file_id:
        db_files_to_retrieve_info = db.query(models.FileToRetrieveRequest)\
            .filter(models.FileToRetrieveRequest.file_id == file_id).all()
    else:
        db_files_to_retrieve_info = db.query(models.FileToRetrieveRequest)\
            .all()
    # If there are no file requests, raise an exception
    if not db_files_to_retrieve_info:
        exception = FilesToRetrieveRequestDoNotExist()
        logging.error(exception.message)
        raise exception
    
    return db_files_to_retrieve_info


def get_file_to_retrieve_status(
        db: Session, 
        file_to_retrieve_status_id: int,
    ) -> models.FileToRetrieveStatus:
    """CRUD Operation to Get the last status or all status of a File To Retrieve

    Args:
        db (Session): database session
        file_to_retrieve_status_id (int): file to retrieve status id in the database

    Returns:
        models.FileToRetrieveStatus: file to retrieve status
    """
    # Get the file to retrieve
    db_file_to_retrieve_status = db.query(models.FileToRetrieveStatus).filter(
        models.FileToRetrieveStatus.file_id == file_to_retrieve_status_id).all()
    print(db_file_to_retrieve_status)
    return db_file_to_retrieve_status


def get_all_files_to_retrieve(db: Session):
    """CRUD Operation to Get all Files To Retrieve from the database

    Args:
        db (Session): database session

    Returns:
        db_files_to_retrieve (list): list with all files from the database
    """
    db_files_to_retrieve = db.query(models.FileToRetrieve).all()

    # If there are no file requests, raise an exception
    #if not db_files_to_retrieve:
    #    exception = FilesToRetrieveDoNotExist()
    #    logging.error(exception.message)
    #    raise exception
    
    return db_files_to_retrieve


def update_file_to_retrieve_status(
    db: Session,
    file_to_retrieve_id: int,
    status: FileToRetrieveStatusEnum
) -> models.FileToRetrieveStatus:
   
    # Get the file to retrieve
    db_file_to_retrieve = db.query(models.FileToRetrieve).filter(
        models.FileToRetrieve.id == file_to_retrieve_id).first()
    
    db_file_to_retrieve_status = models.FileToRetrieveStatus(
            file_id=db_file_to_retrieve.id,
            status=status.value
    )
    
    db.add(db_file_to_retrieve_status)
    db.commit()
    db.refresh(db_file_to_retrieve_status)
    return db_file_to_retrieve_status


def get_files_not_yet_retrieved(db):
    files_not_yet_retrieved = db.query(models.FileToRetrieve)\
        .filter(
            or_(
                models.FileToRetrieve.last_retrieved_timestamp == None,
                models.FileToRetrieve.last_retrieved_timestamp <
                models.FileToRetrieve.last_retrieval_request_time
            ),
            models.FileToRetrieve.was_deleted == False
        ).all()
    
    return files_not_yet_retrieved


def mark_file_as_deleted(db, file_id):
    db_file_to_retrieve = get_file_to_retrieve(db, file_id)
    db_file_to_retrieve.was_deleted = True
    db.commit()
    db.refresh(db_file_to_retrieve)
    logging.info(
        f"File To Retrieve was marked as deleted: {db_file_to_retrieve.as_dict()}.")
    return db_file_to_retrieve


def get_requesters_that_were_not_notified(db, file_id):
    requesters = db.query(models.FileToRetrieveRequest.requesters_email)\
        .filter(
            models.FileToRetrieveRequest.file_id == file_id,
            or_(
                models.FileToRetrieveRequest.requester_informed_timestamp == None,
                models.FileToRetrieveRequest.request_timestamp >
                models.FileToRetrieveRequest.requester_informed_timestamp
            ),
        ).all()
    return [r[0] for r in requesters]


def update_requester_informed_timestamp(db, file_id, requesters_email):
    requesters = db.query(models.FileToRetrieveRequest)\
        .filter(
            models.FileToRetrieveRequest.file_id == file_id,
            models.FileToRetrieveRequest.requesters_email == requesters_email,
        ).all()

    for requester in requesters:
        requester.requester_informed_timestamp = datetime.datetime.now()
        db.commit()
        logging.info(f"File To Retrieve Request was updated: {requester.as_dict()}.")
