import json
import threading
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from services.auth_service.app import angel_session


class AngelWebSocketManager:
    def __init__(self):
        self.sws = None
        self.connected = False
        self.latest_prices = {}  # cache: token -> ltp

    def connect(self):
        conn = angel_session.conn

        if conn is None:
            raise Exception("Angel session not available")

        auth_token = conn.access_token
        api_key = conn.api_key
        client_code = conn.client_code
        feed_token = conn.feed_token

        self.sws = SmartWebSocketV2(
            auth_token=auth_token,
            api_key=api_key,
            client_code=client_code,
            feed_token=feed_token
        )

        # Assign callbacks
        self.sws.on_open = self.on_open
        self.sws.on_data = self.on_data
        self.sws.on_error = self.on_error
        self.sws.on_close = self.on_close

        # Start socket in background thread
        threading.Thread(target=self.sws.connect, daemon=True).start()

    # ================= CALLBACKS =================

    def on_open(self, ws):
        print("✅ Angel WebSocket Connected")
        self.connected = True

    def on_data(self, ws, message):
        data = json.loads(message)

        if "token" in data and "ltp" in data:
            token = data["token"]
            ltp = data["ltp"]

            self.latest_prices[token] = ltp

    def on_error(self, ws, error):
        print("❌ WebSocket Error:", error)
        self.connected = False

    def on_close(self, ws):
        print("🔴 WebSocket Closed")
        self.connected = False

    # ================= SUBSCRIBE =================

    def subscribe(self, tokens, exchange="NSE"):
        """
        tokens = list of symboltoken strings
        """

        if not self.connected:
            print("WebSocket not connected yet")
            return

        token_list = [
            {
                "exchangeType": 1 if exchange == "NSE" else 2,
                "tokens": tokens
            }
        ]

        self.sws.subscribe(
            correlation_id="stream_1",
            mode=1,  # LTP mode
            token_list=token_list
        )

        print("📡 Subscribed to tokens:", tokens)

    def get_ltp(self, token):
        return self.latest_prices.get(token)
