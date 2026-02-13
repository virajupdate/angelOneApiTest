import asyncio
from typing import List, Dict
import time
from services.auth_service.app import angel_session
from SmartApi.smartWebSocketV2 import SmartWebSocketV2

async def user_symbols_ltp(symbols: List[Dict[str, str]]):
    