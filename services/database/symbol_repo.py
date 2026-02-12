from services.database.db import get_connection

def get_all_symbols():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT exchange, tradingsymbol, symboltoken FROM symbols")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def add_symbol(exchange, tradingsymbol, symboltoken):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
       INSERT INTO symbol (exchange, tradingsymbol, symboltoken)
VALUES (?, ?, ?)
    """, (exchange, tradingsymbol, symboltoken))

    conn.commit()
    conn.close()
