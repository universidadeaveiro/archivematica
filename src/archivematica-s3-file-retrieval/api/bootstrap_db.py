# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 16-05-2022 22:28:22
# @Description: 


# generic imports
from fastapi import FastAPI
import logging
import datetime

# custom imports
from sql_app.database import SessionLocal, engine
from sql_app.models import auth_models, s3_glacier_models
import aux.startup as Startup
import sql_app.crud.s3_glacier as S3GlacierCRUD

def main():
    logging.debug("Bootsrapping database...")
    logging.debug("Connecting To Database...")
    # Connect to Database
    MODELS_INITIALIZED = False
    for _ in range(10):
        try:
            auth_models.Base.metadata.create_all(bind=engine)
            s3_glacier_models.Base.metadata.create_all(bind=engine)
            logging.info(f"Tables Created in the Database")
            MODELS_INITIALIZED = True
            break
        except Exception as e:
            logging.error(f"Error while initializing DB: {e}")

    if not MODELS_INITIALIZED:
        exit(2)

    db = SessionLocal()

    # create roles
    Startup.startup_roles(db)
    Startup.create_default_admin(db)
    
    
    # create some files to retrieve
    f1 = S3GlacierCRUD.create_file_to_retrieve(
        db=db,
        bucket_name='arquivo-test-bucket-2',
        file_key='temp/1c08/13ce/102f/4eeb/8d16/67d5/7e3b/8154/glacier-ingest-test-1c0813ce-102f-4eeb-8d16-67d57e3b8154.7z'
    )
    S3GlacierCRUD.update_file_to_retrieve(
        db=db,
        file_to_retrieve_id=f1.id,
        last_retrieval_request_time=datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    )
    f2 = S3GlacierCRUD.create_file_to_retrieve(
        db=db,
        bucket_name='arquivo-test-bucket-2',
        file_key='temp/ab2c/a984/36ad/4796/9e4b/256c/60b7/c071/simple-test-glacier-ab2ca984-36ad-4796-9e4b-256c60b7c071.7z'
    )
    # Create some file to retrieve request
    fr1 = S3GlacierCRUD.create_file_to_retrieve_request(
        db=db,
        file_to_retrieve_id=f1.id,
        requesters_email="rafael.neves.direito@ua.pt"
    )
    fr2 = S3GlacierCRUD.create_file_to_retrieve_request(
        db=db,
        file_to_retrieve_id=f1.id,
        requesters_email="eduardosantoshf@ua.pt"
    )
if __name__ == '__main__':
    main()
