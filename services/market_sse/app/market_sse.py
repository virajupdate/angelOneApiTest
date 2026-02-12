import asyncio
from typing import List, Dict
import time
from services.auth_service.app import angel_session

async def ltp_all(symbols: List[Dict[str, str]]):

    conn = angel_session.conn

    if conn is None:
        yield {"event": "error", "data": "Not logged in"}
        return

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

        await asyncio.sleep(1)
