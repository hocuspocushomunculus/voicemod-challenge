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

from variables import WORKSPACE, voicemod_url, basic_mapping_by_languages, \
    tempmail_url, voicemod_useraccount_url
from locators import accept_cookies_button, background_images, toggle_languages, \
    select_language, email, my_account, email_input_box, continue_with_email_button, \
    verification_code, password_input_box, verify_button, logout_button

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
        self.handles = {"homepage": None, "tempmail": None, "myaccount": None}
        self.TEST_NAME = BuiltIn().get_variable_value("${TEST NAME}")
        self.a_tags = []
        self.images = {"img": [], "background_images": []}
        self.email = None
        self.password = None


    def start_firefox_and_go_to_voicemod_webpage(self):
        """
        Part of test setup, where we configure firefox and navigate to voicemod.net webapp
        """
        # Configure Firefox webdriver
        options = Options()
        options.headless = True
        options.add_argument('no-sandbox')
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/97.0Mozilla/5.0")   # pylint: disable=line-too-long
        self.driver = webdriver.Firefox(options=options,
                                        service_log_path=WORKSPACE + "/results/geckodriver.log")

        # Navigate to voicemod.net and maximize window
        self.driver.get(voicemod_url)
        self.driver.maximize_window()

        # Store reference to voicemod homepage handle
        self.handles["homepage"] = self.driver.window_handles[0]


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
        - img tags
        - anything which has `background-image: url("http(s)://...")` as style
        """
        self.images["img"] = self.driver.find_elements_by_tag_name("img")
        self.images["background_images"] = self.driver.find_elements_by_xpath(background_images)
        self.assertNotEqual(len(self.images["img"]), 0,
                            "Something went wrong, no images found.")
        self.assertNotEqual(len(self.images["background_images"]), 0,
                            "Something went wrong, no background images found.")


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

        # Check tags with background images
        for background_image in self.images["background_images"]:
            style = background_image.get_attribute('style')
            url = re.findall(r"(https?://\S+)['|\"]\)", style)[0]
            r = requests.head(url)

            status_code = r.status_code
            logging.info("%s : %s", url, status_code)
            self.assertEqual(status_code, 200,
                             ("Link to background image "
                              f"at {url} had a status code of {status_code}"))

            # Don't stress the webapp
            time.sleep(0.1)

        logging.info("Successfully checked %s background images, none of them were broken.",
                     len(self.images["background_images"]))


    def switch_to_language_and_do_checks(self, language=""):
        """
        Switch to the language supplied as an argument and check:
        - Page title
        - url
        - save screenshot

        :param language:    str, language to switch to
        """
        # Bring up the language selection menu
        WebDriverWait(self.driver, 10) \
            .until(EC.element_to_be_clickable((By.XPATH, toggle_languages))) \
            .click()

        # Select language
        WebDriverWait(self.driver, 10) \
            .until(EC.element_to_be_clickable((By.XPATH, select_language.format(lang=language)))) \
            .click()

        # Check URL
        current_url = self.driver.current_url
        self.assertEqual(current_url, basic_mapping_by_languages[language]["current_url"],
                         (f"Switching to {language} didn't go as planned: "
                          f"we are at: {current_url}"))

        # Check title
        title = self.driver.title
        self.assertEqual(title, basic_mapping_by_languages[language]["title"],
                         (f"Switching to {language} didn't go as planned: "
                          f"title was: {title}"))

        # Save screenshot
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/{language}.png")


    def store_new_window_handle(self, handle_name):
        """
        Locate the newly opened window (should be adjacent to where the new
        window was opened from) and store it in self.handles with name `handle_name`.

        :param handle_name:     str, name for the key to store the handle with
        """
        new_window_index = self.driver.window_handles.index(self.driver.current_window_handle) + 1
        self.handles[handle_name] = self.driver.window_handles[new_window_index]

        logging.info("Storing handle: '%s' as '%s' (was index %s)",
                     self.driver.window_handles[new_window_index],
                     handle_name, new_window_index)


    def get_temporary_email_address(self):
        """
        Visit temp-mail.org and get a temporary email address. We'll store it
        in self.email class attribute.
        """
        # Open new window, switch to it and open temp-mail.org
        self.driver.execute_script("window.open('');")
        self.store_new_window_handle("tempmail")
        self.driver.switch_to.window(self.handles["tempmail"])
        self.driver.get(tempmail_url)

        # Give 10 seconds for temp-mail.org to load our email address
        time.sleep(10)

        # Get email address
        self.email = self.driver.find_element_by_xpath(email).get_attribute('value')
        logging.info("Using the following email address: %s", self.email)

        # Save screenshot
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/temp-mail.org.png")


    def initiate_registration_to_voicemod(self):
        """
        After having stored a temporary email, initiate the registration
        for a free account at voicemod.net.
        """
        # Make sure to select correct window
        self.driver.switch_to.window(self.handles["homepage"])

        # Get hyperlink from element 'My Account' and open it in new window
        my_account_url = self.driver.find_element_by_xpath(my_account).get_attribute("href")
        self.driver.execute_script("window.open('');")
        self.store_new_window_handle("myaccount")
        self.driver.switch_to.window(self.handles["myaccount"])
        self.driver.get(my_account_url)

        # Save screenshot
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/my_account.png")

        # Register with email
        self.driver.find_element_by_xpath(email_input_box).send_keys(self.email)
        time.sleep(1)
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/my_account_with_email.png")
        self.driver.find_element_by_xpath(continue_with_email_button).click()


    def get_verification_code_from_email(self):
        """
        After we've input our email address into the email input box,
        switch to the temp-mail.org window and scrape the password
        from the verification email.
        """
        # Switch to temp-mail.org window
        self.driver.switch_to.window(self.handles["tempmail"])

        # Wait 10 seconds for the verification email
        time.sleep(10)

        # Get 6-digit password from email
        self.password = \
            re.findall(r"\d{6}", self.driver.find_element_by_xpath(verification_code).text)[0]

        logging.info("Password received by email was: %s", self.password)


    def finish_registration_to_voicemod(self):
        """
        After having received the 6-digit password via email, switch back
        to the myaccount window and input the password.
        """
        # Switch to myaccount window
        self.driver.switch_to.window(self.handles["myaccount"])

        # Input the digits one by one to the appropriate textbox
        for idx, digit in enumerate(self.password):
            self.driver.find_element_by_xpath(password_input_box.format(idx=idx)).send_keys(digit)

        # Save screenshot
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/my_account_with_password.png")

        # Click verify button
        self.driver.find_element_by_xpath(verify_button).click()

        # Wait 2 seconds for redirect
        time.sleep(2)

        # Check url
        self.assertIn(voicemod_useraccount_url, self.driver.current_url,
                      f"Unexpected current url: {self.driver.current_url}")

        # Save screenshot again
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/my_account_logged_in.png")


    def logout_button_visible_and_functional(self):
        """
        After having finished registration, check if there's a logout button
        and if it does log the user out.
        """
        # Locate logout button and click it
        self.driver.find_element_by_xpath(logout_button).click()

        # Check url again
        self.assertNotIn(voicemod_useraccount_url, self.driver.current_url,
                         f"Unexpected current url: {self.driver.current_url}")

        # Save screenshot
        self.driver.save_screenshot(f"results/{self.TEST_NAME}/my_account_logged_out.png")
