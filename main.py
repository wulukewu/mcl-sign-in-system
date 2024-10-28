import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def signInOut(InOrOut):

    # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    # Local Run
    # import json
    # with open('config.json', 'r') as config_file:
    #     config_data = json.load(config_file)
    # username = config_data['username']
    # password = config_data['password']
    # otpauth_url = config_data['otpauth']

    # GitHub Actions
    service = Service(ChromeDriverManager().install())
    username = os.environ['username']
    password = os.environ['password']
    otpauth_url = os.environ['otpauth']
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=options)
    # driver.maximize_window()

    # Login Portal
    driver.get('https://portal.ncu.edu.tw/login')
    time.sleep(.5)

    inputAccount = driver.find_element(By.ID, 'inputAccount')
    inputAccount.click()
    inputAccount.send_keys(username)

    time.sleep(.5)

    inputPassword = driver.find_element(By.ID, 'inputPassword')
    inputPassword.click()
    inputPassword.send_keys(password)
    inputPassword.submit()

    time.sleep(.5)

    from otpauth import otpauth
    otp = otpauth(otpauth_url)

    inputTotp = driver.find_element(By.XPATH, "//input[@id='totp-code']")
    inputTotp.click()
    inputTotp.send_keys(otp)
    inputTotp.submit()

    time.sleep(.5)

    # Enter HumanSys
    driver.get('https://cis.ncu.edu.tw/HumanSys/login')
    time.sleep(.5)

    submit_botton = driver.find_element(By.CLASS_NAME, 'btn-primary')
    submit_botton.click()

    time.sleep(.5)

    driver.get('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn')
    time.sleep(.5)

    # add_signin_button = driver.find_element(By.CLASS_NAME, 'btn-default')
    add_signin_button = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-default')
    add_signin_button.click()

    time.sleep(.5)

    if(InOrOut == 'signin'):

        workContent = driver.find_element(By.ID, 'AttendWork')
        workContent.click()
        workContent.send_keys('MCL工讀')
        time.sleep(.5)

        signin_button = driver.find_element(By.ID, 'signin')
        signin_button.click()
    
    elif(InOrOut == 'signout'):

        signout_button = driver.find_element(By.ID, 'signout')
        signout_button.click()

    else:

        print('Not Correct InOrOut! ')

    time.sleep(.5)
    
    driver.close()
