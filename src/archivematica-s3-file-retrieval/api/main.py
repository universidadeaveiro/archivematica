# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 26-05-2022 22:14:24
# @Description: 


# generic imports
from fastapi import FastAPI
import logging
import inspect
import sys
import os
import time


# custom imports
from sql_app.database import SessionLocal, engine
from routers import s3_glacier, auth
import aux.startup as Startup
import aux.utils as Utils
from sql_app.models import auth_models, s3_glacier_models

logging.debug("Starting up...")

# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

fast_api_tags_metadata = [
    {
        "name": "s3_glacier",
        "description": "Endpoints To Interact with the S3 Glacier",
    },
    {
        "name": "yyy",
        "description": "yyy",
    },
]

fast_api_description = "REST API of the S3 Glacier File Retrieval"

# Start Fast API
app = FastAPI(
    title="S3 Glacier File Retrieval",
    description=fast_api_description,
    version="0.0.1",
    contact={
        "name": "Rafael Direito",
        "email": "rdireito@av.it.pt",
    },
    openapi_tags=fast_api_tags_metadata
)


# Load Routers
app.include_router(s3_glacier.router)
app.include_router(auth.router)

# __init__
@app.on_event("startup")
async def startup_event():

    # Load Config
    ret, message = Startup.load_config()
    if not ret:
        logging.critical(message)
        return exit(1)

    print("Loading Database...")
    # Connect to Database
    MODELS_INITIALIZED = False
    for i in range(10):
        try:
            auth_models.Base.metadata.create_all(bind=engine)
            s3_glacier_models.Base.metadata.create_all(bind=engine)
            MODELS_INITIALIZED = True
            break
        except Exception as e:
            print(f"Error while initializing DB: {e}")

    if not MODELS_INITIALIZED:
        exit(2)

    db = SessionLocal()

    # create roles
    Startup.startup_roles(db)
    Startup.create_default_admin(db)
