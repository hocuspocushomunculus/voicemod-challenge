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
    [Documentation]  Check if latest webapp deployment has
    ...  any broken links (should not have any)
    Collect hyperlink tags on homepage
    Check for broken links


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

