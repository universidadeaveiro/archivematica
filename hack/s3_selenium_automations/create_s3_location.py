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
        ops = webdriver.FirefoxOptions()
        ops.add_argument('--headless')
        self.driver = webdriver.Firefox(options=ops)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_app_dynamics_job(self):
        driver = self.driver
        cas_enabled = False

        # Open Webpage
        print("Accessing Archivematica Storage Service's Web Page")

        if cas_enabled:
            driver.get("https://django-cas-ng-demo-server.herokuapp.com/cas/login?service=http%3A%2F%2Fstic-archivematica.ua.pt%3A443%2Flogin%2F%3Fnext%3D%252F")
        else:
            driver.get("http://stic-archivematica.ua.pt:8080/login/?next=/")

        # Login
        print("Proceeding to Login...")
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()

        if cas_enabled:
            driver.find_element_by_id("id_username").send_keys("admin")
        else:
            driver.find_element_by_id("id_username").send_keys("test")
            driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Administration'])[1]/following::div[1]").click()

        driver.find_element_by_id("id_password").click()
        driver.find_element_by_id("id_password").clear()

        if cas_enabled:
            driver.find_element_by_id("id_password").send_keys("django-cas-ng")
            driver.find_element_by_xpath("//button[@type='submit']").click()
        else:
            driver.find_element_by_id("id_password").send_keys("test")
            driver.find_element_by_xpath("//input[@value='Log in']").click()

        print("Login Successful!")

        # Create S3 Space Location
        print("Creating S3 Space Location...")

        if cas_enabled:
            driver.get("http://stic-archivematica.ua.pt:443/")
        else:
            driver.get("http://stic-archivematica.ua.pt:8080/")
            
        driver.find_element_by_link_text("Spaces").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Actions'])[2]/following::a[1]").click()
        driver.find_element_by_link_text("Create Location here").click()
        driver.find_element_by_id("id_purpose").click()
        Select(driver.find_element_by_id("id_purpose")).select_by_visible_text("AIP Storage")
        driver.find_element_by_id("id_relative_path").click()
        driver.find_element_by_id("id_relative_path").clear()
        driver.find_element_by_id("id_relative_path").send_keys("/temp")
        driver.find_element_by_id("id_description").click()
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("S3 AIP Storage Location")
        driver.find_element_by_xpath("//input[@value='Create Location']").click()
        print("Location Created!")
    
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