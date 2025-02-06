import os
import time
import ffmpeg
import urllib
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import notification as nt

# from dotenv import load_dotenv
# load_dotenv()

def signInOut(InOrOut):
    # Load environ variables
    username = os.getenv('username')
    password = os.getenv('password')

    # Check for OTP availability
    otpauth_url = os.getenv('otpauth')
    hasOTP = True

    if otpauth_url == 'None' or otpauth_url is None:
        hasOTP = False
        print('otpauth_url not detected')

    # Set up ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

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
    actions = ActionChains(driver)

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
        print('[INFO] Return code: 300')
        return 300

    if checkbox_found:
        # switch to recaptcha audio control frame
        time.sleep(1)
        driver.switch_to.default_content()
        frames = driver.find_elements(By.TAG_NAME, 'iframe')

        # click on audio challenge
        time.sleep(1)

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
            print('[INFO] Return code: 300')
            return 300

        if audio_button_found:
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
                # print("\nRetrying to close page and login again...")
                driver.quit()
                # time.sleep(60)
                # signInOut(InOrOut)
                print('[INFO] Return code: 400')
                return 400

            else:
                path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
                path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

                # download the mp3 audio file from the source
                urllib.request.urlretrieve(src, path_to_mp3)

                # Load downloaded mp3 audio file as .wav using ffmpeg
                try:
                    ffmpeg.input(path_to_mp3).output(path_to_wav).run()
                except Exception as e:
                    print(f"[ERR] Failed to convert audio file: {e}")
                    driver.quit()
                    print('[INFO] Return code: 400')
                    return 400

                # translate audio to text with google voice recognition
                time.sleep(3)
                r = sr.Recognizer()

                passcode_recognized = False
                with sr.AudioFile(path_to_wav) as source:
                    audio_file = r.record(source)
                    try:
                        key = r.recognize_google(audio_file, language='en-US', show_all=True)['alternative'][0]['transcript']
                        passcode_recognized = True
                        print(f"[INFO] Recaptcha Passcode: {key}")
                    except sr.UnknownValueError:
                        print("[ERR] Google Speech Recognition could not understand the audio")
                    except sr.RequestError as e:
                        print(f"[ERR] Could not request results from Google Speech Recognition service; {e}")

                # key in results and submit
                if passcode_recognized:
                    time.sleep(3)
                    driver.find_element(By.ID, 'audio-response').send_keys(key.lower())
                    driver.find_element(By.ID, 'audio-response').send_keys(Keys.ENTER)
                    time.sleep(3)
                    driver.switch_to.default_content()
                    time.sleep(3)
                else:
                    print("[ERR] Failed to enter the audio passcode.")
                    driver.quit()
                    print('[INFO] Return code: 500')
                    return 500

    # Press login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
    actions.move_to_element(login_button).click().perform()

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

    try:
        # Try to enter HumanSys
        submit_button = driver.find_element(By.CLASS_NAME, 'btn-primary')
        actions.move_to_element(submit_button).click().perform()
    except:
        # Potentially malicious website
        print('[ERR] Potentially malicious website detected on HumanSys.')
        submit_button = driver.find_element(By.CLASS_NAME, 'btn-danger')
        actions.move_to_element(submit_button).click().perform()
        driver.quit()
        print('[INFO] Return code: 200')
        return 200

    time.sleep(.5)

    driver.get('https://cis.ncu.edu.tw/HumanSys/student/stdSignIn')
    time.sleep(.5)

    # Check for alert message
    try:
        alert_message = driver.find_element(By.XPATH, '//*[@id="form1"]/div')
        print(f'[ERR] {alert_message.text}')
        driver.close()
        print('[INFO] Return code: 100')
        return 100

    except Exception as e:
        print('[INFO] No alert message detected.')

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
        print('[INFO] Return code: 600')
        return 600

    time.sleep(.5)

    driver.close()

    print(f"'{InOrOut}' action completed successfully.")
    print('[INFO] Return code: 000')
    return 000

if __name__ == '__main__':
    # Get inorout from environment, default to "signin"
    inorout = os.getenv('inorout', 'signin')

    # Set retry limit
    retry_limit = 250

    # Retry until successful
    for i in range(retry_limit):
        # Call the signInOut function with the specified action
        result_code = signInOut(inorout)
        print(f"Result code: {result_code}")

        if result_code == 000:
            break

        # time.sleep(60)

    # Send notification to Discord
    discord_token = os.getenv('discord_token')
    guild_id = int(os.getenv('discord_guild_id'))
    channel_id = int(os.getenv('discord_channel_id'))

    if discord_token and guild_id and channel_id:
        message = f"Successfully signed {inorout} with result code {result_code}!"
        print(f"[INFO] Sending message to Discord: {message}")
        nt.dc_send(message, discord_token, guild_id, channel_id)
    else:
        print("[WARN] Discord notification not sent. Missing one or more environment variables.")
