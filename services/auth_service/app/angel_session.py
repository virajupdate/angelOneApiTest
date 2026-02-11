from SmartApi import SmartConnect
from threading import Lock

conn: SmartConnect | None = None
feed_token: str | None = None
client_code: str | None = None

login_lock = Lock()
