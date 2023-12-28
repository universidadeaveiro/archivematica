# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 26-05-2022 22:21:34
# @Description: 

# AUTH
SECRET_KEY = "99cb3e97787cf81a7f418c42b96a06f77ce25ddbb2f7f83a53cf3474896624f9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
DEFAULT_ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "admin"
}
USER_ROLES = ["ADMIN", "USER"]

# Database
DB_NAME = None
DB_LOCATION = None
DB_USER = None
DB_PASSWORD = None


# S3 Glacier
FILE_AVAILABILITY_DAYS = 7
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None
AWS_BUCKET_NAME = None
