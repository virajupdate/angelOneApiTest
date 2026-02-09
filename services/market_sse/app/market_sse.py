import time
from services.auth_service.app.angel_session import conn

def ltp_event_generator():
    if conn is None:
        yield {"event": "error", "data": "Not logged in"}
        return

    symbols = [
        {"exchange": "NSE", "tradingsymbol": "SBIN-EQ", "symboltoken": "3045"},
        {"exchange": "NSE", "tradingsymbol": "RELIANCE-EQ", "symboltoken": "2885"},
    ]

    while True:
        updates = []

        for s in symbols:
            try:
                res = conn.ltpData(
                    exchange=s["exchange"],
                    tradingsymbol=s["tradingsymbol"],
                    symboltoken=s["symboltoken"]
                )

                if res.get("status"):
                    updates.append({
                        "symbol": s["tradingsymbol"],
                        "ltp": res["data"]["ltp"]
                    })

            except Exception as e:
                updates.append({
                    "symbol": s["tradingsymbol"],
                    "error": str(e)
                })

        yield {
            "event": "ltp",
            "data": updates
        }

        time.sleep(1)
