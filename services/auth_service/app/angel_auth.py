import pyotp, os
from dotenv import load_dotenv
from SmartApi import SmartConnect
from services.auth_service.app import angel_session

load_dotenv()

ANGEL_API_KEY = os.getenv("ANGEL_API_KEY")
ANGEL_CLIENT_ID = os.getenv("ANGEL_CLIENT_ID")
ANGEL_PASSWORD = os.getenv("ANGEL_PASSWORD")
ANGEL_TOTP = os.getenv("ANGEL_TOTP_SECRET")

def angel_login():
    with angel_session.login_lock:

        # already logged in → reuse
        if angel_session.conn and angel_session.feed_token:
            return angel_session.conn

        conn = SmartConnect(api_key=ANGEL_API_KEY)

        login = conn.generateSession(
            ANGEL_CLIENT_ID,
            ANGEL_PASSWORD,
            pyotp.TOTP(ANGEL_TOTP).now()
        )

        if not login.get("status"):
            raise RuntimeError(f"Angel login failed: {login}")

        angel_session.conn = conn
        angel_session.feed_token = login["data"]["feedToken"]
        angel_session.client_code = ANGEL_CLIENT_ID

        print("✅ Angel One login successful LOGIN conn id: ", angel_session.conn)

        return conn
