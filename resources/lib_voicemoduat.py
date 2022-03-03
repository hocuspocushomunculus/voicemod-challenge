#!/usr/bin/env python3
"""
Define class methods (keywords) used by VoicemodUAT.robot file here.
"""
import time
import logging
import requests
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
        super().__init__()
        self.driver = None
        self.TEST_NAME = BuiltIn().get_variable_value("${TEST NAME}")
        self.a_tags = []


    def start_firefox_and_go_to_voicemod_webpage(self):
        """
        Part of test setup, where we configure firefox and navigate to voicemod.net webapp
        """
        # Configure Firefox webdriver
        options = Options()
        options.headless = True
        options.add_argument('no-sandbox')
        self.driver = webdriver.Firefox(options=options,
                                        service_log_path=WORKSPACE + "/results/geckodriver.log")

        # Navigate to voicemod.net and maximize window
        self.driver.get(voicemod_url)
        self.driver.maximize_window()

        self.wait_until_page_is_fully_loaded()


    def wait_until_page_is_fully_loaded(self):
        """
        Wait until the page is fully loaded. It will be reused in many situations.
        """
        WebDriverWait(self.driver, 10) \
            .until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        logging.info("Page is fully loaded.")

    def accept_cookies(self):
        """
        Part of test setup, where we wait until we see 'Accept cookies' button        
        """
        
        accept_cookies = WebDriverWait(self.driver, 10) \
            .until(EC.element_to_be_clickable((By.ID, accept_cookies_button)))
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/accept_cookie_visible.png")
        accept_cookies.click()
        time.sleep(1)
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/accept_cookie_not_visible.png")


    def collect_hyperlink_tags_on_homepage(self):
        """
        We collect all the hyperlinks and store it in self.a_tags class attribute
        """
        self.a_tags = self.driver.find_elements_by_tag_name("a")


    def check_for_broken_links(self):
        """
        After having stored the all the hyperlink elements in self.a_tags
        class attribute, visit them one by one.

        We'll visit the urls extracted from the a tags and not click on the
        elements themselves to avoid following error cases:
        `Message: Element <a href="xyz"> could not be scrolled into view`
        """
        status_code_counter = {200: 0, 302: 0}
        for a_tag in self.a_tags:
            url = a_tag.get_attribute('href')
            r = requests.head(url)

            status_code = r.status_code
            logging.info("%s : %s", url, status_code)
            self.assertIn(status_code, [200, 302], f"Link to {url} had a status code of {status_code}")
            status_code_counter[status_code] += 1
            time.sleep(0.01)

        logging.info(("Links working: %s link(s) had a status code of 200"
                      " and %s link(s) had a status code of 302"),
                     status_code_counter[200],
                     status_code_counter[302])