# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 28-05-2022 17:21:03
# @Description: 


# generic imports
from fastapi import FastAPI
import logging
from aux import email


# custom imports
from sql_app.database import SessionLocal, engine
from routers import email, auth
import aux.startup as Startup

logging.debug("Starting up...")

# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

fast_api_tags_metadata = [
    {
        "name": "email",
        "description": "Endpoints Related to Email Sending",
    },
    {
        "name": "user",
        "description": "User Related Endpoints",
    },
]

fast_api_description = "REST API of the S3 Glacier File Retrieval " \
    "Email Notification Service"

# Start Fast API
app = FastAPI(
    title="S3 Glacier File Retrieval - Email Notification Service",
    description=fast_api_description,
    version="0.0.1",
    contact={
        "name": "Rafael Direito",
        "email": "rafael.neves.direito@ua.pt",
    },
    openapi_tags=fast_api_tags_metadata
)


# Load Routers
app.include_router(email.router)
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
    db = SessionLocal()

    # create roles
    Startup.startup_roles(db)
    Startup.create_default_admin(db)
