from services.database.db import get_connection

def add_symbol(exchange, tradingSymbol, symbolToken, redis_client, angel_session):

    ltp = redis_client.hget("ltp_cache", symbolToken)
    if ltp is None:
        try:
            response = angel_session.conn.ltpData(
                exchange=exchange,
                tradingsymbol=tradingSymbol,
                symboltoken=symbolToken
            )
            ltp = response["data"]["ltp"]

            # store in Redis for future
            redis_client.hset("ltp_cache", symbolToken, ltp)

        except Exception:
            ltp = None

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
       INSERT INTO userSymbol (exchange, tradingSymbol, symbolToken, costprice)
VALUES (?, ?, ?)
    """, (exchange, tradingSymbol, symbolToken, ltp))

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
