# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   14-05-2022 19:20:38
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 14-05-2022 22:58:48
# @Description: 


from enum import Enum

class FileToRetrieveStatusEnum(Enum):
    FILE_ADDED_TO_DATABASE = "The file to retrieve from S3 Glacier was added " \
        "to the Retrieval's Service database"
    GLACIER_RETRIEVAL_REQUESTED = "A retrieval process was requested in S3 " \
        "Glacier"
    RETRIEVED_FROM_GLACIER = "The file was retrieved from S3 Glacier"
    RETURNED_TO_GLACIER = "The file stopped being instantly available and " \
        "returned to S3 Glacier"
    REQUESTER_INFORMED_OF_RETRIEVAL = "The requester was informed that the " \
        "file he requested was retrieved from S3 Glacier"

