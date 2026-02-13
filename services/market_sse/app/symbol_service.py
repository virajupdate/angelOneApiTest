import requests
from typing import List, Dict
import sqlite3
from services.database.db import get_connection

MASTER_URL = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"


def sync_master_data():
    print("🌐 Fetching latest master data...")

    response = requests.get(MASTER_URL)
    response.raise_for_status()
    master_data = response.json()

    conn = get_connection()
    cursor = conn.cursor()

    # Convert master data to dict for fast lookup
    master_dict = {
        s["symbol"]: (
            s["exch_seg"],
            s["symbol"],
            s["token"]
        )
        for s in master_data
    }

    # Fetch existing DB records
    cursor.execute("SELECT exchange, tradingSymbol, symbolToken FROM marketSymbol")
    db_rows = cursor.fetchall()

    db_dict = {
        row[1]: (row[0], row[1], row[2])
        for row in db_rows
    }

    master_tokens = set(master_dict.keys())
    db_tokens = set(db_dict.keys())

    # ✅ 1. Insert + Update (UPSERT)
    upsert_data = [
        master_dict[token]
        for token in master_tokens
    ]

    cursor.executemany("""
        INSERT INTO marketSymbol (exchange, tradingSymbol, symbolToken)
        VALUES (?, ?, ?)
        ON CONFLICT(tradingSymbol)
        DO UPDATE SET
            exchange=excluded.exchange,
            symbolToken=excluded.symbolToken
    """, upsert_data)

    # ✅ 2. Delete records not in master
    tokens_to_delete = db_tokens - master_tokens

    if tokens_to_delete:
        cursor.executemany("""
            DELETE FROM marketSymbol WHERE tradingSymbol = ?
        """, [(token,) for token in tokens_to_delete])

    conn.commit()
    conn.close()

    print("✅ Master sync complete")

def get_symbols_by_exchange(exchange: str):
    exchange = exchange.upper()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT exchange, tradingSymbol, symbolToken
        FROM marketSymbol
        WHERE exchange = ?
    """, (exchange,))
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "exchange": row[0],
            "tradingSymbol": row[1],
            "symbolToken": row[2]
        }
        for row in rows
    ]
