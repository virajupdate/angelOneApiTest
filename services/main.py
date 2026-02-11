# services/auth_service/app/main.py
from fastapi import FastAPI, HTTPException
from services.auth_service.app.angel_auth import angel_login
from services.market_sse.app.market_sse import ltp_event_generator
from sse_starlette.sse import EventSourceResponse

app = FastAPI(title="Auth Service")

@app.get("/")
def health():
    return {"status": "ok"}

@app.on_event("startup")
def startup_event():
    try:
        print("🚀 FastAPI startup: logging into Angel One")
        angel_login()
    except Exception as e:
        print(f"Error during Angel login: {e}")
        raise HTTPException(status_code=500, detail="Failed to login to Angel One API")

@app.get("/market/ltp/stream")
def ltp_stream():
    return EventSourceResponse(ltp_event_generator())