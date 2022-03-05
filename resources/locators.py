#!/usr/bin/env python3
"""
Provide locator strings for the robot test.
"""

accept_cookies_button = 'onetrust-accept-btn-handler'
background_images = '//*[contains(@style, "background-image: url(")]'

toggle_languages = '//*[@id="language-selector"]'
select_language = '//*[@id="language-options"]//a[contains(@lang, "{lang}")]'

email = '//*[@id="mail"]'
verification_code = '//a[contains(text(), "Your Voicemod verification code:")]'

my_account = '//a[@title="My Account"]'
email_input_box = '//*[@placeholder="Enter your email"]'
continue_with_email_button = '//button[@data-testid="email-button"]'
password_input_box = '//*[@id="inputBox{idx}"]'
verify_button = '//button[@data-testid="verify-button"]'
logout_button = '//button/span[contains(text(), "Log out")]/parent::button'

voicemod_changer_for_pc = '//a[contains(text(), "Voice Changer for PC")]'
try_it_now = '//a[contains(text(), "TRY IT NOW")]'
