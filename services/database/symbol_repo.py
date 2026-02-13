from services.database.db import get_connection

def add_symbol(exchange, tradingSymbol, symbolToken):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
       INSERT INTO userSymbol (exchange, tradingSymbol, symbolToken)
VALUES (?, ?, ?)
    """, (exchange, tradingSymbol, symbolToken))

    conn.commit()
    conn.close()

def delete_symbol(tradingSymbol):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM userSymbol
        WHERE tradingsymbol = ?
    """, (tradingSymbol,))

    conn.commit()

    rows_deleted = cursor.rowcount
    conn.close()

    return rows_deleted

def get_all_symbols_user():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT exchange, tradingsymbol, symboltoken FROM userSymbol")
    rows = cursor.fetchall()

    conn.close()

    symbols = [
        {
            "exchange": row[0],
            "tradingsymbol": row[1],
            "symboltoken": row[2]
        }
        for row in rows
    ]
    return symbols
