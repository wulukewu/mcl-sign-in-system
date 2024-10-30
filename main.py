import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from dotenv import load_dotenv
load_dotenv()

def signInOut(InOrOut):

    exit_code = 0

    # Load environ
    username = os.environ['username']
    password = os.environ['password']

    hasOTP = True
    try:
        otpauth_url = os.environ['otpauth']
    except:
        print('otpauth_url not detected')
        hasOTP = False

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
        exit_code = 1

    time.sleep(.5)

    driver.close()

    if exit_code == 0:
        print(f"Finished '{InOrOut}' successfully. ")

if __name__ == '__main__':

    try:
        InOrOut = os.environ['inorout']
    except:
        print("No 'InOrOut' set; using default 'signin' instead.")
        InOrOut = 'signin'

    signInOut(InOrOut)