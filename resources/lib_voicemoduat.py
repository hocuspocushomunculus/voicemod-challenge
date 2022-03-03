#!/usr/bin/env python3
"""
Define class methods (keywords) used by VoicemodUAT.robot file here.
"""
import time
import logging
import unittest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from variables import WORKSPACE, voicemod_url
from locators import accept_cookies_button

from robot.libraries.BuiltIn import BuiltIn


class lib_voicemoduat(unittest.TestCase):
    """
    Class to contain attributes and keywords used during UAT testing of Voicemod webapp.
    """
    def __init__(self):
        """
        Initialize some class attributes
        """
        self.driver = None
        self.TEST_NAME = BuiltIn().get_variable_value("${TEST NAME}")


    def start_firefox_and_go_to_voicemod_webpage(self):
        """
        Part of test setup, where we configure firefox and navigate to voicemod.net webapp
        """
        # Configure Firefox webdriver
        options = Options()
        options.headless = True
        options.add_argument('no-sandbox')
        self.driver = webdriver.Firefox(options=options, service_log_path=WORKSPACE + "/results/geckodriver.log")

        # Navigate to voicemod.net and maximize window
        self.driver.get(voicemod_url)
        self.driver.maximize_window()

        # Wait until page is fully loaded
        WebDriverWait(self.driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')


    def accept_cookies(self):
        """
        Part of test setup, where we wait until we see 'Accept cookies' button        
        """
        
        accept_cookies = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, accept_cookies_button)))
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/accept_cookie_visible.png")
        accept_cookies.click()
        time.sleep(1)
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/accept_cookie_not_visible.png")
