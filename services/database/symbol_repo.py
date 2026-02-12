from services.database.db import get_connection
from services.market_sse.app.market_sse import ltp_all
from sse_starlette.sse import EventSourceResponse

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

def get_all_ltp_user():
    symbolsList = get_all_symbols_user()
    print('Checkout the list of all symbols from get_all_symbols', symbolsList)
    return EventSourceResponse(ltp_all(symbolsList))
