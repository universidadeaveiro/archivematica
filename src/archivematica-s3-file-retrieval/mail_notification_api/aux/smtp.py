# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   29-05-2022 12:39:49
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 29-05-2022 12:52:04
# @Description: 

import aux.constants as Constants
import smtplib
import certifi
import ssl

class SMTPWrapper:
        
    def __init__ (self):
        self.session = self.create_new_session()
    
    
    def create_new_session(self):
        # Create a secure SSL context
        context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH,
            cafile=certifi.where()
        )
        # Create an smtp connection with tls
        self.session = smtplib.SMTP(
            Constants.NOTIFICATION_EMAIL_SMTP_SERVER,
            Constants.NOTIFICATION_EMAIL_SMTP_PORT
        )
        self.session.starttls(context=context)
        # Login
        self.session.login(
            Constants.NOTIFICATION_EMAIL_ADDRESS,
            Constants.NOTIFICATION_EMAIL_PASSWORD
        )


    def update_session(self):
        try: status = self.session.noop()[0]
        except: status = -1 # smtplib.SMTPServerDisconnected
            
        if status != 250:
            self.create_new_session()
        
        
    def send_email(self, sender, recipients, message):
        self.update_session()
        self.session.sendmail(sender, recipients, message.as_string())
        
