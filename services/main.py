# services/auth_service/app/main.py
from fastapi import FastAPI, HTTPException
from services.auth_service.app.angel_auth import angel_login
from services.market_sse.app.market_sse import ltp_event_generator
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter
from services.database.symbol_repo import add_symbol
from services.database.db import createSymbolTable
from pydantic import BaseModel

app = FastAPI(title="Auth Service")

@app.get("/")
def health():
    return {"status": "ok"}

@app.on_event("startup")
def startup_event():
    try:
        print("🚀 FastAPI startup: logging into Angel One")
        angel_login()
        createSymbolTable()
    except Exception as e:
        print(f"Error during Angel login: {e}")
        raise HTTPException(status_code=500, detail="Failed to login to Angel One API")

@app.get("/market/ltp/stream")
def ltp_stream():
    return EventSourceResponse(ltp_event_generator())

symbolRouter = APIRouter(prefix="/symbols")

class SymbolCreate(BaseModel):
    exchange: str
    tradingsymbol: str
    symboltoken: str

@symbolRouter.post("/add")
def create_symbol(symbol: SymbolCreate):
    add_symbol(
        symbol.exchange,
        symbol.tradingsymbol,
        symbol.symboltoken
    )
    return {"status": "Symbol added"}

app.include_router(symbolRouter)