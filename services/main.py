# services/auth_service/app/main.py
from fastapi import FastAPI, HTTPException
from services.auth_service.app.angel_auth import angel_login
from services.market_sse.app.market_sse import ltp_event_generator
from sse_starlette.sse import EventSourceResponse

app = FastAPI(title="Auth Service")

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/auth/angel/login")
def login():
    try:
        data = angel_login()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/market/ltp/stream")
def ltp_stream():
    return EventSourceResponse(ltp_event_generator())