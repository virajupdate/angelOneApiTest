from SmartApi import SmartConnect
from threading import Lock

conn: SmartConnect | None = None
feed_token: str | None = None
client_code='AACD685864'

login_lock = Lock()
