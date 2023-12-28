# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   28-05-2022 11:37:00
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 28-05-2022 11:37:13
# @Description: 



class FileToRetreiveDoesNotExist(Exception):

    def __init__(self, file_id=None):
        if file_id:
            self.file_id = file_id
            self.message = f"The File to Retrieve with ID={self.file_id} " \
                "doesn't exist"
        else:
           self.message = "The File to Retrieve Doesn't Exist"
        super().__init__(self.message)

    def __str__(self):
        return self.message

class FilesToRetrieveDoNotExist(Exception):

    def __init__(self, file_id=None):
        self.message = "There are no Files To Retrieve"

        super().__init__(self.message)

    def __str__(self):
        return self.message
        
class FilesToRetrieveRequestDoNotExist(Exception):

    def __init__(self, file_id=None):
        self.message = "There are no File To Retrieve Requests"

        super().__init__(self.message)

    def __str__(self):
        return self.message
