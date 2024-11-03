import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
import argparse
from dotenv import load_dotenv

# import sys
import re
import urllib
import pydub
import speech_recognition as sr
from selenium.webdriver.common.keys import Keys

load_dotenv()

def signInOut(InOrOut):
    # Load environ variables
    username = os.getenv('username')
    password = os.getenv('password')

    # Check for OTP availability
    otpauth_url = os.getenv('otpauth')
    hasOTP = True
    if otpauth_url == 'None':
        hasOTP = False
        print('otpauth_url not detected')

    # Set up ChromeDriver
    service = Service('/usr/local/bin/chromedriver')
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

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
    # inputPassword.submit()

    time.sleep(.5)

    # Solve reCAPTCHA
    # frames = driver.find_elements_by_tag_name("iframe")
    frames = driver.find_elements(By.TAG_NAME, 'iframe')
    recaptcha_control_frame = None
    recaptcha_challenge_frame = None
    for index, frame in enumerate(frames):
        if re.search('reCAPTCHA', frame.get_attribute("title")):
            recaptcha_control_frame = frame
            
        if re.search('recaptcha challenge', frame.get_attribute("title")):
            recaptcha_challenge_frame = frame
    if not (recaptcha_control_frame and recaptcha_challenge_frame):
        print("[ERR] Unable to find recaptcha. Abort solver.")
        # sys.exit()
    # switch to recaptcha frame
    time.sleep(.5)
    # frames = driver.find_elements_by_tag_name("iframe")
    frames = driver.find_elements(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(recaptcha_control_frame)
    # click on checkbox to activate recaptcha
    # driver.find_element_by_class_name("recaptcha-checkbox-border").click()
    driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border').click()

    # switch to recaptcha audio control frame
    time.sleep(5)
    # delay()
    driver.switch_to.default_content()
    # frames = driver.find_elements_by_tag_name("iframe")
    frames = driver.find_elements(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(recaptcha_challenge_frame)

    # click on audio challenge
    time.sleep(10)
    # driver.find_element_by_id("recaptcha-audio-button").click()
    # driver.find_element(By.ID, 'recaptcha-audio-button').click()

    # Use JavaScript to click the element
    element = driver.find_element(By.ID, 'recaptcha-audio-button')
    driver.execute_script("arguments[0].click();", element)

    try:
        # switch to recaptcha audio challenge frame
        driver.switch_to.default_content()
        # frames = driver.find_elements_by_tag_name("iframe")
        frames = driver.find_elements(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(recaptcha_challenge_frame)

        # get the mp3 audio file
        # delay()
        time.sleep(5)
        # src = driver.find_element_by_id("audio-source").get_attribute("src")
        src = driver.find_element(By.ID, 'audio-source').get_attribute('src')
        print(f"[INFO] Audio src: {src}")

        path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
        path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

        # download the mp3 audio file from the source
        urllib.request.urlretrieve(src, path_to_mp3)

        # load downloaded mp3 audio file as .wav
        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
        sound.export(path_to_wav, format="wav")
        sample_audio = sr.AudioFile(path_to_wav)

        # translate audio to text with google voice recognition
        # delay()
        time.sleep(5)
        r = sr.Recognizer()
        with sample_audio as source:
            audio = r.record(source)
        key = r.recognize_google(audio)
        print(f"[INFO] Recaptcha Passcode: {key}")

        # key in results and submit
        # delay()
        time.sleep(5)
        # driver.find_element_by_id("audio-response").send_keys(key.lower())
        driver.find_element(By.ID, 'audio-response').send_keys(key.lower())
        # driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
        driver.find_element(By.ID, 'audio-response').send_keys(Keys.ENTER)
        time.sleep(5)
        driver.switch_to.default_content()
        time.sleep(5)
        # driver.find_element_by_id("recaptcha-demo-submit").click()
        driver.find_element(By.ID, 'recaptcha-demo-submit').click()
        # if (tor_process):
        #     tor_process.kill()

        # Finished reCAPTCHA solving with audio challenge.
        print('Finished reCAPTCHA solving with audio challenge.')

    except:
        # Finished reCAPTCHA solving without audio challenge.
        print('Finished reCAPTCHA solving without audio challenge.')
        pass

    # # auto locate recaptcha frames
    # try:
    #     # delay()
    #     time.sleep(5)
    #     # frames = driver.find_elements_by_tag_name("iframe")
    #     frames = driver.find_elements(By.TAG_NAME, 'iframe')
    #     recaptcha_control_frame = None
    #     recaptcha_challenge_frame = None
    #     for index, frame in enumerate(frames):
    #         if re.search('reCAPTCHA', frame.get_attribute("title")):
    #             recaptcha_control_frame = frame
                
    #         if re.search('recaptcha challenge', frame.get_attribute("title")):
    #             recaptcha_challenge_frame = frame
    #     if not (recaptcha_control_frame and recaptcha_challenge_frame):
    #         print("[ERR] Unable to find recaptcha. Abort solver.")
    #         # sys.exit()
    #     # switch to recaptcha frame
    #     # delay()
    #     time.sleep(5)
    #     # frames = driver.find_elements_by_tag_name("iframe")
    #     frames = driver.find_elements(By.TAG_NAME, 'iframe')
    #     driver.switch_to.frame(recaptcha_control_frame)
    #     # click on checkbox to activate recaptcha
    #     # driver.find_element_by_class_name("recaptcha-checkbox-border").click()
    #     driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border').click()
    
    #     # switch to recaptcha audio control frame
    #     # delay()
    #     time.sleep(5)
    #     driver.switch_to.default_content()
    #     # frames = driver.find_elements_by_tag_name("iframe")
    #     frames = driver.find_elements(By.TAG_NAME, 'iframe')
    #     driver.switch_to.frame(recaptcha_challenge_frame)
    
    #     # click on audio challenge
    #     time.sleep(10)
    #     # driver.find_element_by_id("recaptcha-audio-button").click()
    #     driver.find_element(By.ID, 'recaptcha-audio-button').click()
    
    #     # switch to recaptcha audio challenge frame
    #     driver.switch_to.default_content()
    #     # frames = driver.find_elements_by_tag_name("iframe")
    #     frames = driver.find_elements(By.TAG_NAME, 'iframe')
    #     driver.switch_to.frame(recaptcha_challenge_frame)
    
    #     # get the mp3 audio file
    #     # delay()
    #     time.sleep(5)
    #     # src = driver.find_element_by_id("audio-source").get_attribute("src")
    #     src = driver.find_element(By.ID, 'audio-source').get_attribute('src')
    #     print(f"[INFO] Audio src: {src}")
    
    #     path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
    #     path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))
    
    #     # download the mp3 audio file from the source
    #     urllib.request.urlretrieve(src, path_to_mp3)
    # except:
    #     # if ip is blocked.. renew tor ip
    #     print("[INFO] IP address has been blocked for recaptcha.")
    #     # if activate_tor:
    #     #     renew_ip(CONTROL_PORT)
    #     # sys.exit()    

    # # load downloaded mp3 audio file as .wav
    # try:
    #     sound = pydub.AudioSegment.from_mp3(path_to_mp3)
    #     sound.export(path_to_wav, format="wav")
    #     sample_audio = sr.AudioFile(path_to_wav)
    # except Exception:
    #     # sys.exit(
    #     #     "[ERR] Please run program as administrator or download ffmpeg manually, "
    #     #     "https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/"
    #     # )
    #     pass

    # # translate audio to text with google voice recognition
    # try:
    #     # delay()
    #     time.sleep(5)
    #     r = sr.Recognizer()
    #     with sample_audio as source:
    #         audio = r.record(source)
    #     key = r.recognize_google(audio)
    #     print(f"[INFO] Recaptcha Passcode: {key}")
    # except: pass

    # # key in results and submit
    # try:
    #     # delay()
    #     time.sleep(5)
    #     # driver.find_element_by_id("audio-response").send_keys(key.lower())
    #     driver.find_element(By.ID, 'audio-response').send_keys(key.lower())
    #     # driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
    #     driver.find_element(By.ID, 'audio-response').send_keys(Keys.ENTER)
    #     time.sleep(5)
    #     driver.switch_to.default_content()
    #     time.sleep(5)
    #     # driver.find_element_by_id("recaptcha-demo-submit").click()
    #     driver.find_element(By.ID, 'recaptcha-demo-submit').click()
    #     # if (tor_process):
    #     #     tor_process.kill()
    # except: pass

    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
    login_button.click()
    
    time.sleep(5)
    # return

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
    os.environ['otpauth'] = args.otpauth or 'None'

    signInOut(args.inorout)