# services/auth_service/app/angel_auth.py
import requests
from SmartApi import SmartConnect
import pyotp
import os
from dotenv import load_dotenv
from services.auth_service.app.angel_session import conn

load_dotenv()

ANGEL_API_KEY = str(os.getenv("ANGEL_API_KEY"))
ANGEL_CLIENT_ID = os.getenv("ANGEL_CLIENT_ID")
ANGEL_PASSWORD = str(os.getenv("ANGEL_PASSWORD"))
ANGEL_TOTP = str(os.getenv("ANGEL_TOTP_SECRET"))

def angel_login():
    global conn
    try:
        conn = SmartConnect(api_key=ANGEL_API_KEY)

        login = conn.generateSession(
            ANGEL_CLIENT_ID,
            ANGEL_PASSWORD,
            pyotp.TOTP(ANGEL_TOTP).now()
        )
        if not login.get("status"):
            raise RuntimeError(f"Login failed: {login}")

        print('Login Success')
        conn.setAccessToken(login["data"]["jwtToken"])
        return {
            "jwtToken": login["data"]["jwtToken"],
            "refreshToken": login["data"]["refreshToken"],
            "feedToken": login["data"]["feedToken"],
            "clientCode": ANGEL_CLIENT_ID
        }
    except Exception as e:
        print(f"Error during login: {e}")
        raise   