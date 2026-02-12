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
            symboltoken TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()