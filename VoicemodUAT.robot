*** Settings ***
Library    SeleniumLibrary
Variables  resources/variables.yaml

*** Test Cases ***
Firefox
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].firefox.webdriver.Options()    sys, selenium.webdriver
    Call Method    ${options}   add_argument      -headless
    Call Method    ${options}   add_argument      -no-sandbox
    Create Webdriver    Firefox    options=${options}  service_log_path=${WORKSPACE}/results/geckodriver.log
    Set Window Size    1500    1500
    Go To    https://spage.fi
    Capture Page Screenshot
    [Teardown]    Close All Browsers
