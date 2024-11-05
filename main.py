import os
import time
import re
import urllib
import argparse
from dotenv import load_dotenv
import ffmpeg
import speech_recognition as sr

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    # service = Service('/usr/local/bin/chromedriver')
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(executable_path='./venv/bin/chromedriver-win64/chromedriver.exe', options=options)

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

    actions = ActionChains(driver)

    # try:
    time.sleep(1)
    frames = driver.find_elements(By.TAG_NAME, 'iframe')
    # recaptcha_control_frame = None
    # recaptcha_challenge_frame = None
    # for index, frame in enumerate(frames):
    #     if re.search('reCAPTCHA', frame.get_attribute("title")):
    #         recaptcha_control_frame = frame
            
    #     if re.search('recaptcha challenge', frame.get_attribute("title")):
    #         recaptcha_challenge_frame = frame
    # if not (recaptcha_control_frame and recaptcha_challenge_frame):
    #     print("[ERR] Unable to find recaptcha. Abort solver.")
        # sys.exit()
    # switch to recaptcha frame
    time.sleep(1)
    frames = driver.find_elements(By.TAG_NAME, 'iframe')

    # Iterate through all frames to find the checkbox to activate recaptcha
    checkbox_found = False
    for index, frame in enumerate(frames):
        driver.switch_to.frame(frame)
        try:
            checkbox = driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border')
            checkbox.click()
            print(f"[INFO] Found and clicked checkbox in frame {index}")
            checkbox_found = True
            break
        except Exception as e:
            print(f"[DEBUG] Frame {index} does not contain the checkbox: {e}")
            driver.switch_to.default_content()

    if not checkbox_found:
        print("[ERR] Unable to find the checkbox in any frame.")
        driver.quit()
        return
    # time.sleep(1)
    # frames = driver.find_elements(By.TAG_NAME, 'iframe')
    # # driver.switch_to.frame(recaptcha_control_frame)
    # driver.switch_to.frame(frames[0])
    # # click on checkbox to activate recaptcha
    # driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border').click()

    # switch to recaptcha audio control frame
    time.sleep(1)
    driver.switch_to.default_content()
    frames = driver.find_elements(By.TAG_NAME, 'iframe')
    # driver.switch_to.frame(recaptcha_challenge_frame)
    # driver.switch_to.frame(frames[0])

    # click on audio challenge
    time.sleep(1)
    # driver.find_element(By.ID, 'recaptcha-audio-button').click()
    # driver.find_element(By.CLASS_NAME, 'rc-button-audio').click()
    # driver.find_element(By.XPATH, '//button[@id="recaptcha-audio-button"]').click()
    # Iterate through all frames to find the audio challenge button
    audio_button_found = False
    for index, frame in enumerate(frames):
        driver.switch_to.frame(frame)
        try:
            audio_button = driver.find_element(By.ID, 'recaptcha-audio-button')
            audio_button.click()
            print(f"[INFO] Found and clicked audio button in frame {index}")
            audio_button_found = True
            break
        except:
            driver.switch_to.default_content()

    if not audio_button_found:
        print("[ERR] Unable to find the audio challenge button in any frame.")
        driver.quit()
        return

    # switch to recaptcha audio challenge frame
    time.sleep(1)
    driver.switch_to.default_content()
    frames = driver.find_elements(By.TAG_NAME, 'iframe')

    # Iterate through all frames to find the audio source
    audio_source_found = False
    for index, frame in enumerate(frames):
        driver.switch_to.frame(frame)
        try:
            src = driver.find_element(By.ID, 'audio-source').get_attribute('src')
            print(f"[INFO] Audio src found in frame {index}: {src}")
            audio_source_found = True
            break
        except:
            driver.switch_to.default_content()

    if not audio_source_found:
        print("[ERR] Unable to find the audio source in any frame.")
        driver.quit()
        return

    path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
    path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

    # download the mp3 audio file from the source
    urllib.request.urlretrieve(src, path_to_mp3)

    # # switch to recaptcha audio challenge frame
    # driver.switch_to.default_content()
    # frames = driver.find_elements(By.TAG_NAME, 'iframe')
    # # driver.switch_to.frame(recaptcha_challenge_frame)
    # driver.switch_to.frame(frames[0])

    # # get the mp3 audio file
    # time.sleep(3)
    # # src = driver.find_element_by_id("audio-source").get_attribute("src")
    # src = driver.find_element(By.ID, 'audio-source').get_attribute('src')
    # # src = driver.find_element(By.CLASS, 'rc-button-audio').get_attribute('src')
    # print(f"[INFO] Audio src: {src}")

    # path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
    # path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

    # # download the mp3 audio file from the source
    # urllib.request.urlretrieve(src, path_to_mp3)
    # except:
    #     # if ip is blocked.. renew tor ip
    #     print("[INFO] IP address has been blocked for recaptcha.")
    #     if activate_tor:
    #         renew_ip(CONTROL_PORT)
    #     sys.exit()    

    # load downloaded mp3 audio file as .wav
    # try:
    # pydub.AudioSegment.ffmpeg = './venv/bin'

    # Download the mp3 audio file from the source
    urllib.request.urlretrieve(src, path_to_mp3)

    # Load downloaded mp3 audio file as .wav using ffmpeg
    # try:
    ffmpeg.input(path_to_mp3).output(path_to_wav).run(cmd='./venv/bin/ffmpeg/bin/ffmpeg.exe')
    sample_audio = sr.AudioFile(path_to_wav)
    # except Exception as e:
    #     print(f"[ERR] Failed to convert audio file: {e}")
    #     driver.quit()
    #     return

    # sound = pydub.AudioSegment.from_mp3(path_to_mp3)
    # sound.export(path_to_wav, format="wav")
    # sample_audio = sr.AudioFile(path_to_wav)
    # except Exception:
    #     # sys.exit(
    #     #     "[ERR] Please run program as administrator or download ffmpeg manually, "
    #     #     "https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/"
    #     # )
    #     print('[ERR] Please run program as administrator or download ffmpeg manually, https://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/')
    #     pass

    # translate audio to text with google voice recognition
    time.sleep(3)
    r = sr.Recognizer()
    # with sample_audio as source:
    #     audio = r.record(source)
    # key = r.recognize_google(audio)
    # print(f"[INFO] Recaptcha Passcode: {key}")

    with sr.AudioFile(path_to_wav) as source:
        audio_file = r.record(source)
        try:
            key = r.recognize_google(audio_file, language='en-US', show_all=True)
            print("I think you said '" + r.recognize_google(audio_file) + "'")
        except sr.UnknownValueError:
            print("[ERR] Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"[ERR] Could not request results from Google Speech Recognition service; {e}")

    # key in results and submit
    time.sleep(3)
    # driver.find_element_by_id("audio-response").send_keys(key.lower())
    driver.find_element(By.ID, 'audio-response').send_keys(key.lower())
    # driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
    driver.find_element(By.ID, 'audio-response').send_keys(Keys.ENTER)
    time.sleep(3)
    driver.switch_to.default_content()
    time.sleep(3)
    driver.find_element_by_id("recaptcha-demo-submit").click()
    # if (tor_process):
    #     tor_process.kill()

    # Solve reCAPTCHA
    # frames = driver.find_elements(By.TAG_NAME, 'iframe')
    # recaptcha_control_frame = None
    # recaptcha_challenge_frame = None
    # for index, frame in enumerate(frames):
    #     if re.search('reCAPTCHA', frame.get_attribute("title")):
    #         recaptcha_control_frame = frame
            
    #     if re.search('recaptcha challenge', frame.get_attribute("title")):
    #         recaptcha_challenge_frame = frame
    # if not (recaptcha_control_frame and recaptcha_challenge_frame):
    #     print("[ERR] Unable to find recaptcha. Abort solver.")
    #     # return

    # try:
    #     # Switch to recaptcha frame
    #     time.sleep(.5)
    #     driver.switch_to.frame(recaptcha_control_frame)
    #     recaptcha_checkbox = driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border')

    #     # Move cursor to the reCAPTCHA checkbox and click
    #     actions.move_to_element(recaptcha_checkbox).click().perform()

    # except Exception as e:
    #     print(f"[ERR] Unable to find the reCAPTCHA checkbox. Abort solver: \n{e}")
    #     # print("[ERR] Unable to find the reCAPTCHA checkbox. Abort solver.")
    #     pass

    # try:
    #     # Switch to recaptcha audio control frame
    #     time.sleep(3)
    #     driver.switch_to.default_content()
    #     frames = driver.find_elements(By.TAG_NAME, 'iframe')
    #     driver.switch_to.frame(recaptcha_challenge_frame)

    #     # Click on audio challenge
    #     time.sleep(10)
    #     audio_button = driver.find_element(By.ID, 'recaptcha-audio-button')
    #     actions.move_to_element(audio_button).click().perform()
    # except Exception as e:
    #     print(f"[ERR] Unable to find the audio challenge button. Abort solver: \n{e}")
    #     # print("[ERR] Unable to find the audio challenge button. Abort solver.")
    #     pass

    # try:
    #     # Switch to recaptcha audio challenge frame
    #     driver.switch_to.default_content()
    #     frames = driver.find_elements(By.TAG_NAME, 'iframe')
    #     driver.switch_to.frame(recaptcha_challenge_frame)

    #     # Get the mp3 audio file
    #     time.sleep(3)
    #     src = driver.find_element(By.ID, 'audio-source').get_attribute('src')
    #     print(f"[INFO] Audio src: {src}")

    #     path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
    #     path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

    #     # Download the mp3 audio file from the source
    #     urllib.request.urlretrieve(src, path_to_mp3)

    #     # Load downloaded mp3 audio file as .wav
    #     sound = pydub.AudioSegment.from_mp3(path_to_mp3)
    #     sound.export(path_to_wav, format="wav")
    #     sample_audio = sr.AudioFile(path_to_wav)

    #     # Translate audio to text with google voice recognition
    #     time.sleep(3)
    #     r = sr.Recognizer()
    #     with sample_audio as source:
    #         audio = r.record(source)
    #     key = r.recognize_google(audio)
    #     print(f"[INFO] Recaptcha Passcode: {key}")

    #     # Key in results and submit
    #     time.sleep(3)
    #     driver.find_element(By.ID, 'audio-response').send_keys(key.lower())
    #     driver.find_element(By.ID, 'audio-response').send_keys(Keys.ENTER)
    #     time.sleep(3)
    #     driver.switch_to.default_content()
    #     time.sleep(3)

    #     # Wait for the submit button to be present
    #     try:
    #         WebDriverWait(driver, 10).until(
    #             EC.presence_of_element_located((By.ID, 'recaptcha-demo-submit'))
    #         )
    #         driver.find_element(By.ID, 'recaptcha-demo-submit').click()
    #     except Exception as e:
    #         print("[ERR] Unable to find the submit button. Abort solver: \n{e}")
    #         # print("[ERR] Unable to find the submit button. Abort solver.")

    #     # Finished reCAPTCHA solving with audio challenge.
    #     print('Finished reCAPTCHA solving with audio challenge.')

    # except Exception as e:
    #     # Finished reCAPTCHA solving without audio challenge.
    #     print(f'Finished reCAPTCHA solving without audio challenge: \n{e}')
    #     # print(f'Finished reCAPTCHA solving without audio challenge.')
    #     pass

    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
    actions.move_to_element(login_button).click().perform()
    
    time.sleep(3)

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
    actions.move_to_element(submit_botton).click().perform()

    time.sleep(.5)

    driver.get('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn')
    time.sleep(.5)

    # Sign-in or sign-out actions
    add_signin_button = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-default')
    actions.move_to_element(add_signin_button).click().perform()

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
