import pyotp
from urllib.parse import urlparse, parse_qs

def otpauth(otpauth_url):

    # 解析 otpauth URL
    parsed_url = urlparse(otpauth_url)
    params = parse_qs(parsed_url.query)

    # 從 URL 中提取 secret
    secret = params['secret'][0]

    # 使用 secret 生成 OTP
    totp = pyotp.TOTP(secret)
    otp = totp.now()

    print("Your OTP is:", otp)
    return otp