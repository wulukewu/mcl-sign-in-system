import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import argparse
from dotenv import load_dotenv
load_dotenv()

def signInOut(InOrOut):

    # Load environ variables
    username = os.getenv('username')
    password = os.getenv('password')

    # Check for OTP availability
    otpauth_url = os.getenv('otpauth')
    hasOTP = bool(otpauth_url)
    if not hasOTP:
        print('otpauth_url not detected')

    # Set up ChromeDriver
    options = Options()
    options.headless = True  # Enable headless mode
    #driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'), options=options)
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

    if hasOTP:
        from otpauth import otpauth
        otp = otpauth(otpauth_url)

        inputTotp = driver.find_element(By.ID, 'totp-code')
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

    # Sign-in or sign-out actions
    add_signin_button = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-default')
    add_signin_button.click()

    time.sleep(.5)

    if InOrOut == 'signin':
        workContent = driver.find_element(By.ID, 'AttendWork')
        workContent.click()
        workContent.send_keys('MCL工讀')
        time.sleep(.5)

        signin_button = driver.find_element(By.ID, 'signin')
        signin_button.click()
    
    elif InOrOut == 'signout':
        signout_button = driver.find_element(By.ID, 'signout')
        signout_button.click()

    else:
        print('Invalid InOrOut option! Please specify "signin" or "signout".')
        driver.close()
        return

    time.sleep(.5)

    driver.close()

    print(f"'{InOrOut}' action completed successfully.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inorout', default="signin", help="Specify 'signin' or 'signout' (default: 'signin')")
    parser.add_argument('--username', required=True, help="Username for login")
    parser.add_argument('--password', required=True, help="Password for login")
    parser.add_argument('--otpauth', required=False, help="OTP authentication URL")
    args = parser.parse_args()

    os.environ['username'] = args.username
    os.environ['password'] = args.password
    os.environ['otpauth'] = args.otpauth or None

    signInOut(args.inorout)