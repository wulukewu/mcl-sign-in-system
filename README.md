# MCL Automatic Sign-in System

![GitHub last commit](https://img.shields.io/github/last-commit/wulukewu/mcl-sign-in-system?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/wulukewu/mcl-sign-in-system?style=for-the-badge)
![Docker Pulls](https://img.shields.io/docker/pulls/wulukewu/mcl-sign-in-system?style=for-the-badge)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/wulukewu/mcl-sign-in-system/latest?label=latest%20image%20size&style=for-the-badge)

An auto sign-in/sign-out system for NCU HumanSys. 

## Hub

**GitHub**: [wulukewu/mcl-sign-in-system](https://github.com/wulukewu/mcl-sign-in-system)

**Docker Hub**: [wulukewu/mcl-sign-in-system](https://hub.docker.com/r/wulukewu/mcl-sign-in-system)

## Quick Start

Run the container with the following command, replacing `your_username`, `your_password`, and `your_otpauth_url` with your actual credentials:

```bash
docker run -e username=your_username \
           -e password=your_password \
           -e otpauth=your_otpauth_url \
           -e inorout=signout \
           wulukewu/mcl-sign-in-system:latest
```

To sign in instead of signing out (which is the default), omit the `-e inorout=signout` line.  Also, omit the `-e otpauth=your_otpauth_url` line if you don't use OTP.

## Secrets Configuration (GitHub Actions)

If you're using GitHub Actions, add the following secrets under your repository settings:

- `username`: Your Student ID used for login.
- `password`: Password for your portal login.
- `otpauth` [optional]: OTP URL to generate a one-time password (OTP) for two-factor authentication.

Remember to adjust the `inorout` value as needed.

## Parameters

The following parameters are configured using environment variables.  These can be set using the `-e` flag when running `docker run` or by defining them in your shell environment.

- **`inorout`**: Specify `"signin"` or `"signout"` for the desired action. Defaults to `"signin"` if not specified.
- **`username`**: Your Student ID used for login.
- **`password`**: Password for your portal login.
- **`otpauth`** [optional]: OTP URL to generate a one-time password (OTP) for two-factor authentication.  If not provided, OTP authentication will be skipped.  Set to `"None"` if you do not use OTP.

## Usage

To run the script *directly* (outside of Docker), you must set the required environment variables *before* executing the `python main.py` command. The method for setting environment variables depends on your operating system and shell. Here are a few examples:

**Linux/macOS (Bash):**

```bash
export username=your_username
export password=your_password
export otpauth=your_otpauth_url
export inorout=signout  # Optional, defaults to signin
python main.py
```

**Windows (Command Prompt):**

```cmd
set username=your_username
set password=your_password
set otpauth=your_otpauth_url
set inorout=signout  # Optional, defaults to signin
python main.py
```

**Windows (PowerShell):**

```powershell
$env:username="your_username"
$env:password="your_password"
$env:otpauth="your_otpauth_url"
$env:inorout="signout" # Optional, defaults to signin
python main.py
```

**Important:**  Remember to replace `your_username`, `your_password`, and `your_otpauth_url` with your actual values. The `export` (Linux/macOS) or `set` (Windows) commands set the environment variables for the current shell session.

## Docker

To build and run the Docker container, use the following commands.  Make sure to replace `your_username`, `your_password`, and `your_otpauth_url` with your actual credentials.

```sh
docker build -t mcl-sign-in-system .
docker run -e username=your_username \
           -e password=your_password \
           -e otpauth=your_otpauth_url \
           -e inorout=signout \
           mcl-sign-in-system
```

If you want to sign in, you can omit the `-e inorout=signout` line, as the default value is `"signin"`.

## Return Codes

The script will return the following codes to indicate the outcome of the execution:

- `000`: Successfully completed the sign-in or sign-out action.
- `100`: Alert message detected, nothing to do.
- `200`: Potentially malicious website detected.
- `300`: Failed to solve reCAPTCHA.
- `400`: Failed to find the audio source for reCAPTCHA.
- `500`: Failed to enter the audio passcode.
- `600`: Invalid `inorout` option.

## References

- [VS Code + Python + Selenium Automation Testing Part 1](https://medium.com/begonia-design/vs-code-python-selenium-%E8%87%AA%E5%8B%95%E5%8C%96%E6%B8%AC%E8%A9%A6-part-1-30d6c0ea92af)
- [Day 15: Dynamic Web Page Scraping 2 - Selenium Data Location Functions](https://ithelp.ithome.com.tw/articles/10300961)
- [【 Python 】利用 .env 與環境變數隱藏敏感資訊](https://learningsky.io/python-use-environmental-variables-to-hide-sensitive-information/)
- [Pull a certain branch from the remote server](https://stackoverflow.com/questions/1709177/pull-a-certain-branch-from-the-remote-server)
- [recaptcha_v2_solver](https://github.com/ohyicong/recaptcha_v2_solver)
