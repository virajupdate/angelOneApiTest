# services/auth_service/app/main.py
from fastapi import FastAPI, HTTPException
from services.auth_service.app.angel_auth import angel_login
from fastapi import APIRouter, Query
from services.database.symbol_repo import add_symbol, delete_symbol, get_all_ltp_user, get_all_symbols_user
from services.database.db import createUserSymbolTable
from services.market_sse.app.symbol_service import get_symbols_by_exchange
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
        createUserSymbolTable()
    except Exception as e:
        print(f"Error during Angel login: {e}")
        raise HTTPException(status_code=500, detail="Failed to login to Angel One API")

symbolRouter = APIRouter(prefix="/symbols")

class symbolCreate(BaseModel):
    exchange: str
    tradingSymbol: str
    symbolToken: str

@symbolRouter.post("/add")
def create_symbol(symbol: symbolCreate):
    add_symbol(
        symbol.exchange,
        symbol.tradingSymbol,
        symbol.symbolToken
    )
    return {"status": "Symbol added"}

class symbolDelete(BaseModel):
    tradingSymbol: str

@symbolRouter.post("/delete")
def remove_symbol(symbol: symbolDelete):
    rows_deleted = delete_symbol(symbol.tradingSymbol)

    if rows_deleted == 0:
        return {"message": "Symbol not found"}

    return {"message": "Symbol deleted successfully"}

@symbolRouter.get("/display/user/all")
def display_all_symbols_user():
    symbols=get_all_symbols_user()
    return symbols

@symbolRouter.get("/ltp/user/all")
def fetch_all_ltp():
    return get_all_ltp_user()

@symbolRouter.get("/by-market")
def fetch_symbols_by_market(
    market: str = Query(..., description="NSE or BSE")):
    return get_symbols_by_exchange(market)

app.include_router(symbolRouter)