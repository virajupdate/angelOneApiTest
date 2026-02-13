import requests
from typing import List, Dict
import sqlite3
from services.database.db import get_connection

MASTER_URL = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"


def load_master_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM marketSymbol")
    count = cursor.fetchone()[0]

    if count > 0:
        print("✅ Loading symbols from DB")
        conn.close()
        return

    print("🌐 Fetching master from URL...")
    response = requests.get(MASTER_URL)
    response.raise_for_status()
    data = response.json()

    # Insert into DB
    symbols = [
        (s["exch_seg"], s["symbol"], s["token"])
        for s in data
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO marketSymbol
        (exchange, tradingsymbol, symboltoken)
        VALUES (?, ?, ?)
    """, symbols)

    conn.commit()
    conn.close()

    print("✅ Master data inserted into DB")


def get_symbols_by_exchange(exchange: str):
    exchange = exchange.upper()
    conn = get_connection()
    cursor = conn.cursor()

    load_master_data()

    cursor.execute("""
        SELECT exchange, tradingsymbol, symboltoken
        FROM marketSymbol
        WHERE exchange = ?
    """, (exchange,))
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "exchange": row[0],
            "tradingsymbol": row[1],
            "symboltoken": row[2]
        }
        for row in rows
    ]
