from services.database.db import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS symbols (
            exchangeRate TEXT NOT NULL,
            tradingSymbol TEXT NOT NULL,
            symbolToken TEXT PRIMARY KEY NOT NULL,
            UNIQUE(symbolToken, tradingSymbol)
        )
    """)

    conn.commit()
    conn.close()
