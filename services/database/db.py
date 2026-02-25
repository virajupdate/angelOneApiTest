import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "trading.db"

print(f"Database path: {DB_PATH}")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def createUserSymbolTable():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS userSymbol (
            exchange TEXT NOT NULL,
            tradingsymbol TEXT PRIMARY KEY NOT NULL,
            symboltoken TEXT NOT NULL,
            costprice INT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def createMarketSymbolTable():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marketSymbol (
            exchange TEXT NOT NULL,
            tradingSymbol TEXT PRIMARY KEY NOT NULL,
            symbolToken TEXT NOT NULL
        )
    """)

    cursor.execute("""CREATE INDEX IF NOT EXISTS idx_tradingSymbol
            ON marketSymbol(tradingsymbol);""")

    conn.commit()
    conn.close()