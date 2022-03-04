*** Settings ***
Library    OperatingSystem
Library    SeleniumLibrary
Variables  resources/locators.py
Variables  resources/variables.py

Library    resources/lib_voicemoduat.py

Test Setup      Test Setup
Test Teardown   Test Teardown

*** Test Cases ***
Test 1 - There are no broken links
    [Documentation]  Locate all hyperlinks (<a> tags)
    ...  on the homepage (voicemod.net) and check for
    ...  any broken links (status code should be 200 or 302)
    Locate hyperlink tags on homepage
    Check for broken links

Test 2 - There are no broken images
    [Documentation]  Locate all images on the homepage (voicemod.net)
    ...  and check if all of them load properly,
    ...  (status code should be 200).
    Locate images on homepage
    Check for broken images

Test 3 - User is able to switch languages
    [Documentation]  Locate the element to toggle languages.
    ...  Then switch the language and do some preliminary checks:
    ...  - check url
    ...  - check title
    ...  - take screenshot
    Switch to Language and do checks  language=fr
    Switch to Language and do checks  language=ja
    Switch to Language and do checks  language=ru
    Switch to Language and do checks  language=es
    Switch to Language and do checks  language=ko
    Switch to Language and do checks  language=zh

*** Keywords ***
Test Setup
    [Documentation]  Tasks to do before each and every test case
    ...  - Create directory for each test case where we'll store some of the results.
    ...  - Load voicemod.net in Firefox & accept cookies
    Create Directory  ${WORKSPACE}/results/${TEST NAME}

    Start Firefox And Go To Voicemod Webpage
    Accept Cookies


Test Teardown
    [Documentation]  Tasks to do after each and every test case
    Close All Browsers
