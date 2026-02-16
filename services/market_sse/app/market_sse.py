import asyncio
from typing import List, Dict
import time
from services.auth_service.app import angel_session
from SmartApi.smartWebSocketV2 import SmartWebSocketV2

from typing import List, Dict
import asyncio
from services.market_sse.app.ws_manager import angelWebSocketManager


async def user_symbols_ltp(symbols: List[Dict[str, str]]):
    webSocketObj = angelWebSocketManager()
    if not symbols:
        return []

    tokens = [s["symboltoken"] for s in symbols]

    # Subscribe (only new ones)
    if webSocketObj.connected:
        webSocketObj.subscribe(tokens)

    # Fetch all LTPs in ONE redis call
    ltps = webSocketObj.redis_client.hmget("ltp_cache", tokens)

    response = []

    for symbol, ltp in zip(symbols, ltps):
        response.append({
            "symbol": symbol["tradingsymbol"],
            "token": symbol["symboltoken"],
            "exchange": symbol["exchange"],
            "ltp": float(ltp) if ltp else None
        })

    return response
