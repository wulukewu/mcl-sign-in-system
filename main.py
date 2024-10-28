import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

import json
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
username = config_data['username']
password = config_data['password']

driver = webdriver.Chrome()
# driver.maximize_window()

driver.get('https://portal.ncu.edu.tw/login')
# driver.get('https://cis.ncu.edu.tw/HumanSys/')

inputAccount = driver.find_element(By.ID, 'inputAccount')
inputAccount.send_keys(username)

inputPassword = driver.find_element(By.ID, 'inputPassword')
inputPassword.send_keys(password)

inputPassword.submit()

# os._exit(0)
time.sleep(10)