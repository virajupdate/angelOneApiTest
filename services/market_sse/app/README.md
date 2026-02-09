Angel One API (REST / WebSocket)
        |
        |  (poll / ws)
        v
FastAPI Market Service
        |
        |  (Server-Sent Events)
        v
Browser / UI / Client

Why SSE?

One-way data (server → client) ✅

Perfect for LTP streaming

No reconnect mess like WebSockets

Works great with FastAPI