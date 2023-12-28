# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   28-05-2022 17:55:25
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 28-05-2022 18:00:38
# @Description: 


class AuthenticationFailed(Exception):

    def __init__(self, url=None):
        if url:
            self.url = url
            self.message = f"Impossible to authenticate in the Email "\
                f"Notification API ({self.url})!"
        else:
           self.message = "Impossible to authenticate in the Email Notification API!"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class CouldNotRequestEmailNotification(Exception):

    def __init__(self, file_key=None):
        if file_key:
            self.file_key = file_key
            self.message = f"Impossible to request a new Email "\
                f"Notification for file ({self.file_key})!"
        else:
           self.message = "Impossible to request a new Email Notification!"
        super().__init__(self.message)

    def __str__(self):
        return self.message
