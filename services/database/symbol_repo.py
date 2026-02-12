from services.database.db import get_connection

def get_all_symbols():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT exchange, tradingsymbol, symboltoken FROM symbols")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def add_symbol(exchange, tradingSymbol, symbolToken):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
       INSERT INTO symbol (exchange, tradingSymbol, symbolToken)
VALUES (?, ?, ?)
    """, (exchange, tradingSymbol, symbolToken))

    conn.commit()
    conn.close()

def delete_symbol(tradingSymbol):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM symbols
        WHERE tradingsymbol = ?
    """, (tradingSymbol,))

    conn.commit()

    rows_deleted = cursor.rowcount
    conn.close()

    return rows_deleted

