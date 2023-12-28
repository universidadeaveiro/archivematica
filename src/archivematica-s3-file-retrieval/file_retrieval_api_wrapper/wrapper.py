# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   30-05-2022 20:23:10
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 01-06-2022 20:25:46
# @Description: 

from file_retrieval_api_wrapper.api_requests import MailAPIRequests
from file_retrieval_api_wrapper import file_contents

class FileRetrievalAPIWrapper:
    api_requests = None
    
    def __init__(self, host, username, password) -> None:
        self.api_requests = MailAPIRequests(host, username, password)
        pass
    
    def request_retrieval(self, local_file_path, bucket, file_key, requester):
        try:
            self.api_requests.retrieve_file(
                bucket,
                file_key,
                requester
            )
            
            f = open(local_file_path, 'w')
            f.write(file_contents.OK_TEXT)
            f.close()

        except Exception as e:
            print(f"Exception occured -> {e}")
            f = open(local_file_path, 'w')
            f.write(file_contents.NOT_OK_TEXT)
            f.close()
