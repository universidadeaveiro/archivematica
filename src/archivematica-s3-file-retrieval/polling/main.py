# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   14-05-2022 14:05:32
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 29-05-2022 16:03:43
# @Description: 
import datetime 
import re
import logging
import boto3
import botocore
import sql_app.database as database
from typing import Union
from aux import startup
import aux.constants as Constants
from sql_app import crud
import time
from aux.file_to_retrieve_status import FileToRetrieveStatusEnum
from mail_api_wrapper import mail_api_wrapper
# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)


def check_if_file_has_been_retrieved(s3, db, file) -> Union [bool, datetime.datetime]:
    """Function to check if a file has been retrieved from Glacier
    Args:
        s3 (_type_): s3 client object
        db (_type_): database session object
        file (_type_): file to retrieve object
    Returns:
        Union [bool, datetime.datetime]: 1st argument -> True if file has been
        restored, False otherwise. 2nd argument -> expiry date of the file, in 
        case it has been restored.
    """
    try:
        file_object = s3.Object(file.bucket_name, file.file_key)
        logging.info(f"The following file was retrieved from S3: {file_object}")

        if file_object.storage_class == "GLACIER":
            logging.info(f"File {file_object} is on the glacier storage class")

            # if has been restored
            if "expiry-date" in file_object.restore:
                time_str = re.search(
                    r"expiry-date=\"(.*)\"",
                    file_object.restore
                )
                time_str = time_str.group(1).split(",")[1].split("GMT")[0].strip()
                expiry_date = datetime.datetime.strptime(
                    time_str, 
                    '%d %b %Y %H:%M:%S'
                )
                return True, expiry_date
            return False, ""
        else:
            logging.info(f"File {file_object} is not on the glacier storage class")

    # if file doesn't exist anymore
    except botocore.exceptions.ClientError as e:
        if "Not Found" in str(e):
            logging.info("File can't be found, perhaps it was deleted")
            crud.mark_file_as_deleted(db, file.id)
        return False, ""
    except Exception as e:
        logging.error(f"Error: {e}")
        return False, ""        
    


def get_files_retrieval_status(db, s3) -> None:
    """Function to query S3 Glacier for all files that haven't been retrieved
    yet and check if there's any update on their retrieval status
    Args:
        s3 (_type_): s3 client object
        db (_type_): database session object
    """
    files_not_yet_retrieved = crud.get_files_not_yet_retrieved(db)

    logging.info(f"Files not yet retrieved: {files_not_yet_retrieved}")

    all_files_to_retrieve = crud.get_all_files_to_retrieve(db)

    logging.info(f"All files to retrieve: {all_files_to_retrieve}")

    if not files_not_yet_retrieved:
        logging.info("There are no files to be retrieved")
    
    for f in files_not_yet_retrieved:
        logging.info(f"The following file was not yet retrieved: {f}")
        
        restored, expiry_date = check_if_file_has_been_retrieved(s3, db, f)
        
        # if file has been restored
        if restored:
            
            logging.info(f"File (bucket_name={f.bucket_name},"
                f" file_key={f.file_key}) has been restored!"
                )
            logging.info("Informing its requesters...")

            # ask for notification e-mail
            requesters = list(
                set(crud.get_requesters_that_were_not_notified(db, f.id))
            )

            mail_api_wrapper.send_notification_email(f.file_key, requesters)

            logging.info("The following requesters were informed that the file they "
                         f"requested is ready for download: {requesters}.")
            
            # update db
            # update last_retrieved_timestamp and timestamp_of_file_removal
            crud.update_file_to_retrieve(
                db = db,
                file_to_retrieve_id = f.id, 
                last_retrieved_timestamp = datetime.datetime.now(),
                timestamp_of_file_removal = expiry_date
            )
            # update file to retrieve status to 'RETRIEVED_FROM_GLACIER'
            crud.update_file_to_retrieve_status(
                db=db,
                file_to_retrieve_id=f.id,
                status=FileToRetrieveStatusEnum.RETRIEVED_FROM_GLACIER
            )
            
            
            
 

def main():
    # Load all needed variables/config
    startup.load_config()
    
    polling_interval_secs = Constants.POLLING_INTERVAL_HOURS * 3600
    
    while True:
        # Create S3 client and get retrieved already files
        s3 = boto3.resource('s3',
            aws_access_key_id=Constants.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Constants.AWS_SECRET_ACCESS_KEY
        )

        logging.info("Running File Retrieve Polling...")
        get_files_retrieval_status(database.session, s3)
        # Sleep for a while
        logging.info(f"Polling will sleep for {Constants.POLLING_INTERVAL_HOURS} "\
            "hours...")
        time.sleep(polling_interval_secs)
    
    
if __name__ == "__main__":
   main()