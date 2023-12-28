# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 29-05-2022 13:29:48
# @Description: 

# AUTH
SECRET_KEY = "99cb3e97787cf81a7f418c42b96a06f77ce25ddbb2f7f83a53cf3474896624f9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
DEFAULT_ADMIN_CREDENTIALS = {
    "username": "email-notification-admin",
    "password": "admin"
}
USER_ROLES = ["ADMIN", "USER"]

# Email Notification Service
NOTIFICATION_EMAIL_SMTP_SERVER = None
NOTIFICATION_EMAIL_SMTP_PORT = None
NOTIFICATION_EMAIL_ADDRESS= None
NOTIFICATION_EMAIL_PASSWORD = None
CONTACT_EMAIL = None
FILE_AVAILABILITY_DAYS = None