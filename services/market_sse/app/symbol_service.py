import requests
from typing import List, Dict

MASTER_URL = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"

_symbols_cache: List[Dict] = []


def load_master_data():
    global _symbols_cache

    if not _symbols_cache:
        response = requests.get(MASTER_URL)
        response.raise_for_status()
        _symbols_cache = response.json()

    return _symbols_cache


def get_symbols_by_exchange(exchange: str):
    exchange = exchange.upper()

    data = load_master_data()

    filtered = [
        {
            "exchange": s["exch_seg"],
            "tradingsymbol": s["symbol"],
            "symboltoken": s["token"]
        }
        for s in data
        if s["exch_seg"] == exchange
    ]

    return filtered
