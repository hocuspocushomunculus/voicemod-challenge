#!/usr/bin/env python3
"""
Define class methods (keywords) used by VoicemodUAT.robot file here.
"""
import re
import time
import logging
import unittest
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from variables import WORKSPACE, voicemod_url
from locators import accept_cookies_button

from robot.libraries.BuiltIn import BuiltIn

# pylint: disable=invalid-name

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
        self.images = {"img": [], "page-container": []}


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
        Part of test setup, where we wait until we see 'Accept cookies' button.
        """
        accept_cookies = WebDriverWait(self.driver, 10) \
            .until(EC.element_to_be_clickable((By.ID, accept_cookies_button)))
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/accept_cookie_visible.png")
        accept_cookies.click()
        time.sleep(1)
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/accept_cookie_not_visible.png")


    def locate_hyperlink_tags_on_homepage(self):
        """
        We locate all the hyperlinks and store it in self.a_tags class attribute
        """
        self.a_tags = self.driver.find_elements_by_tag_name("a")

        self.assertNotEqual(len(self.a_tags), 0, "Something went wrong, no hyperlinks found.")


    def check_for_broken_links(self):
        """
        After having stored the all the hyperlink elements in self.a_tags
        class attribute, check them one by one.

        We should get either 200 or 302 as a response/status code.
        """
        status_code_counter = {200: 0, 302: 0}
        for a_tag in self.a_tags:
            url = a_tag.get_attribute('href')
            r = requests.head(url)

            status_code = r.status_code
            logging.info("%s : %s", url, status_code)
            self.assertIn(status_code, [200, 302],
                          f"Link to {url} had a status code of {status_code}")
            status_code_counter[status_code] += 1
            
            # Don't stress the webapp
            time.sleep(0.1)

        logging.info(("Links working: %s link(s) had a status code of 200"
                      " and %s link(s) had a status code of 302"),
                     status_code_counter[200],
                     status_code_counter[302])


    def locate_images_on_homepage(self):
        """
        We locate all the images and store it in self.images class attribute.
        """
        self.images["img"] = self.driver.find_elements_by_tag_name("img")
        self.images["page-container"] = \
            self.driver.find_elements_by_class_name("page-container")

        self.assertNotEqual(len(self.images["img"]), 0,
                            "Something went wrong, no images found.")
        self.assertNotEqual(len(self.images["page-container"]), 0,
                            "Something went wrong, no page-containers found.")


    @staticmethod
    def parse_image_url(img):
        """
        Given a selenium element, get the `src` or `data-src` attribute
        and return an url.

        :param img:     selenium.webdriver.remote.webelement.WebElement
        :return:        str, parsed out url.
        """
        # Try with `src` first
        url = img.get_attribute('src')

        # Try `data-src` next
        if not url:
            url = img.get_attribute('data-src')

        if not url:
            alt = img.get_attribute('alt')
            BuiltIn().fatal_error(("Fatal error: could not locate source for"
                                   f" image `{alt}`"))

        return url


    def check_for_broken_images(self):
        """
        After having stored all the images in self.images class attribute,
        check them one by one if they are properly loaded.
        """
        # Check 'img' tags
        for img in self.images["img"]:
            url = self.parse_image_url(img)
            r = requests.head(url)

            status_code = r.status_code
            logging.info("%s : %s", url, status_code)
            self.assertEqual(status_code, 200,
                             f"Link to image at {url} had a status code of {status_code}")

            # Don't stress the webapp
            time.sleep(0.1)

        logging.info("Successfully checked %s images, none of them were broken.",
                     len(self.images["img"]))

        # Check tags with class 'page-container'
        for page_container in self.images["page-container"]:
            style = page_container.get_attribute('style')
            url = re.findall(r"(https?://\S+)['|\"]\)", style)[0]
            r = requests.head(url)

            status_code = r.status_code
            logging.info("%s : %s", url, status_code)
            self.assertEqual(status_code, 200,
                             ("Link to image (inside a page-container) "
                              f"at {url} had a status code of {status_code}"))

            # Don't stress the webapp
            time.sleep(0.1)

        logging.info("Successfully checked %s images, none of them were broken.",
                     len(self.images["page-container"]))
