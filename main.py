import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

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
    username = os.environ['username']
    password = os.environ['password']
    otpauth_url = os.environ['otpauth']
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    driver = webdriver.Chrome()
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

    inputTotp = driver.find_element(By.ID, 'totp-code')
    inputTotp.click()
    inputTotp.send_keys(otp)
    inputTotp.submit()

    time.sleep(.5)

    # Enter HumanSys
    driver.get('https://cis.ncu.edu.tw/HumanSys/login')

    submit_botton = driver.find_element(By.CLASS_NAME, 'btn-primary')
    submit_botton.click()

    driver.get('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn')

    # add_signin_button = driver.find_element(By.CLASS_NAME, 'btn-default')
    add_signin_button = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-default')
    add_signin_button.click()

    if(InOrOut == 'signin'):

        workContent = driver.find_element(By.ID, 'AttendWork')
        workContent.click()
        workContent.send_keys('MCL工讀')

        signin_button = driver.find_element(By.ID, 'signin')
        signin_button.click()
    
    elif(InOrOut == 'signout'):

        signout_button = driver.find_element(By.ID, 'signout')
        signout_button.click()

    else:

        print('Not Correct InOrOut! ')

    driver.close()
