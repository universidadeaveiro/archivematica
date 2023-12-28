# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 14-05-2022 23:02:14
# @Description: 

# generic imports
from pydantic import BaseModel

class NewFileRetrieval(BaseModel):
    file_key: str
    bucket_name: str
    requesters_email: str

