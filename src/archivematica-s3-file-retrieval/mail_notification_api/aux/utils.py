# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 28-05-2022 16:40:32
# @Description: 


# generic imports
from datetime import datetime
from email import message
from fastapi.responses import JSONResponse
import logging
import aux.constants as Constants
# custom imports

# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

response_dict = {
    "message": "",
    "data": [],
    "errors": [],
    "sucess": True
}

def create_response(status_code=200, data=[], errors=[], success=True, message=""):
    return JSONResponse(status_code=status_code, content={"message": message, "success": success, 
    "data": data, "errors": errors}, headers={"Access-Control-Allow-Origin": "*"})

