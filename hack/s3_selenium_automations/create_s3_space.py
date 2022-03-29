# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        print("Starting driver... ")
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        print("Driver is Running")
    
    def test_app_dynamics_job(self):
        driver = self.driver

        # Open Webpage
        print("Accessing Archivematica Storage Service's Web Page")
        driver.get("https://django-cas-ng-demo-server.herokuapp.com/cas/login?service=http%3A%2F%2Fstic-archivematica.ua.pt%3A443%2Flogin%2F%3Fnext%3D%252F")

        # Login
        print("Proceeding to Login...")
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("django-cas-ng")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        print("Login Successful!")

        # Create S3 Space
        print("Creating S3 Space...")
        driver.get("http://stic-archivematica.ua.pt:443/")
        driver.find_element_by_link_text("Spaces").click()
        driver.find_element_by_link_text("Create new space").click()
        driver.find_element_by_id("id_space-access_protocol").click()
        Select(driver.find_element_by_id("id_space-access_protocol")).select_by_visible_text("S3")
        driver.find_element_by_id("id_space-staging_path").click()
        driver.find_element_by_id("id_space-staging_path").clear()
        driver.find_element_by_id("id_space-staging_path").send_keys("/var/uploads")
        driver.find_element_by_id("id_protocol-endpoint_url").click()
        driver.find_element_by_id("id_protocol-endpoint_url").clear()
        driver.find_element_by_id("id_protocol-endpoint_url").send_keys("https://s3.amazonaws.com/")
        driver.find_element_by_id("id_protocol-access_key_id").click()
        driver.find_element_by_id("id_protocol-access_key_id").clear()
        driver.find_element_by_id("id_protocol-access_key_id").send_keys("AKIAZO2DUK2II4UOXX2E")
        driver.find_element_by_id("id_protocol-secret_access_key").click()
        driver.find_element_by_id("id_protocol-secret_access_key").clear()
        driver.find_element_by_id("id_protocol-secret_access_key").send_keys("asUosGrZaRz4LQ2soydiHxCtrRtj1LbdpZIaL7Cm")
        driver.find_element_by_id("id_protocol-region").click()
        driver.find_element_by_id("id_protocol-region").clear()
        driver.find_element_by_id("id_protocol-region").send_keys("eu-west-3")
        driver.find_element_by_id("id_protocol-bucket").click()
        driver.find_element_by_id("id_protocol-bucket").clear()
        driver.find_element_by_id("id_protocol-bucket").send_keys("arquivo-test-bucket")
        driver.find_element_by_xpath("//input[@value='Create Space']").click()
        print("Space Created!")
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()