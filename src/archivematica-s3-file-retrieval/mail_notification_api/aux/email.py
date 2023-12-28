# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   28-05-2022 16:55:03
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 29-05-2022 13:36:19
# @Description: 
import textwrap
import aux.constants as Constants
from email.mime.text import MIMEText
from enum import Enum

class EmailType(Enum):
    RETRIEVAL_REQUEST_SENT = "retrieval_request_sent"
    FILE_RETRIEVED = "file_retrieved"


class Email:
    
    email_from = "Arquivo Geral da Universidade de Aveiro"
    
    def __init__(self, email_type, file_key):
        self.email_type = email_type
        self.file_key = file_key
        self.archival_package_name = self.file_key.split("/")[-1]
        
    
    def get_subject(self):
        if self.email_type == EmailType.RETRIEVAL_REQUEST_SENT.value:
            return f"Archivematica - Pedido de recuperação de arquivo - {self.archival_package_name}"
        elif self.email_type == EmailType.FILE_RETRIEVED.value:
            return f"Archivematica - Arquivo disponível para download - {self.archival_package_name}"
    
    def get_body(self):
        body = None

        if self.email_type == EmailType.RETRIEVAL_REQUEST_SENT.value:
             body = textwrap.dedent(f"""\
        Ex.mo(a) Senhor(a), 
        
        O arquivo '{self.archival_package_name}', que tentou obter através do Archivematica, não está imediatamente disponível.
        Estamos, neste momento, a trabalhar para recuperar o mesmo, sendo que nas próximas 24h deverá receber um e-mail a notificá-lo de que o arquivo está disponível para download. 
        
        Caso não receba este e-mail, por favor, contacte-nos através do email {Constants.CONTACT_EMAIL}.
        
        Após receber o e-mail de notificação, o arquivo ficará disponível por {Constants.FILE_AVAILABILITY_DAYS} dias.
        Posteriormente, o mesmo será movido para arquivo profundo.
        
        Obrigado,
        Arquivo Geral da Universidade de Aveiro

        -----------------------------

        Hello, 

        ....
        < mensagem em ingles aqui>
        """)
        elif self.email_type == EmailType.FILE_RETRIEVED.value:
            body = textwrap.dedent(f"""\
        Ex.mo(a) Senhor(a), 
        
        O arquivo '{self.archival_package_name}', que tentou obter através do Archivematica, está disponível para download.
        Para obter este arquivo deve seguir os mesmos passos que realizou aquando o pedido do mesmo.
        
        Caso não consiga fazer o download do mesmo, contacte-nos através do e-mail {Constants.CONTACT_EMAIL}.
        
        Relembramos que o arquivo apenas ficará disponível para download por {Constants.FILE_AVAILABILITY_DAYS} dias.
        
        Obrigado,
        Arquivo Geral da Universidade de Aveiro

        -----------------------------

        Hello, 

        ....
        < mensagem em ingles aqui>
        """)
        return body
        
    def compose_email(self):
        msg = MIMEText(self.get_body())
        msg['Subject'] = self.get_subject()
        msg['From'] = self.email_from
        
        return msg

