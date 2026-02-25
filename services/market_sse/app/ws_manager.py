import json
import threading
import redis
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from services.auth_service.app import angel_session


class angelWebSocketManager:
    def __init__(self, angel_session):
        self.sws = None
        self.connected = False
        self.angel_session = angel_session

        # 🔥 Redis connection (shared state)
        self.redis_client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True  # returns str instead of bytes
        )

    # ================= CONNECT =================

    def connect(self):
        conn = self.angel_session

        if conn is None:
            raise Exception("Angel session not available")

        self.sws = SmartWebSocketV2(
            auth_token=conn.access_token,
            api_key=conn.api_key,
            client_code=angel_session.client_code,
            feed_token=conn.feed_token
        )

        # Assign callbacks
        self.sws.on_open = self.on_open
        self.sws.on_data = self.on_data
        self.sws.on_error = self.on_error
        self.sws.on_close = self.on_close

        # Run websocket in background thread
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

            # 🔥 Store in Redis HASH
            # Key: ltp_cache
            # Field: token
            # Value: ltp
            self.redis_client.hset("ltp_cache", token, ltp)

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

    # ================= READ LTP =================

    def get_ltp(self, token):
        """
        Fetch latest price from Redis
        """
        return self.redis_client.hget("ltp_cache", token)
