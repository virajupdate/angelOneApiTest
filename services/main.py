# services/auth_service/app/main.py
from fastapi import FastAPI, HTTPException
from services.auth_service.app.angel_auth import angel_login
from fastapi import APIRouter, Query
from services.database.symbol_repo import add_symbol, delete_symbol, get_all_symbols_user
from services.database.db import createUserSymbolTable, createMarketSymbolTable
from services.market_sse.app.symbol_service import get_symbols_by_exchange, sync_master_data
from services.market_sse.app.market_sse import user_symbols_ltp
from services.market_sse.app.ws_manager import angelWebSocketManager
from services.auth_service.app.angel_session import client_code
from pydantic import BaseModel
from fastapi import Request

app = FastAPI(title="Auth Service")

@app.get("/")
def health():
    return {"status": "ok"}



@app.on_event("startup")
async def startup_event():
    try:
        print("🚀 FastAPI startup: logging into Angel One")
        angel_session = angel_login()
        createUserSymbolTable()
        createMarketSymbolTable()
        sync_master_data()
        angelOneManager = angelWebSocketManager(angel_session)
        angelOneManager.connect()
        app.state.ws_manager = angelOneManager
        app.state.angel_session = angel_session
    except Exception as e:
        print(f"Error during Angel login: {e}")
        raise HTTPException(status_code=500, detail="Failed to login to Angel One API")

symbolRouter = APIRouter(prefix="/symbols")



@symbolRouter.post("/add")
def add_symbol_user(exchange: str, tradingSymbol: str, symbolToken: str, request: Request):
    redis_client = request.app.state.ws_manager.redis_client
    add_symbol(
        exchange=exchange,
        tradingSymbol=tradingSymbol,
        symbolToken=symbolToken,
        redis_client=redis_client,
        angel_session = request.app.state.angel_session
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
    print(symbols)
    return symbols

@symbolRouter.get("/ltp/user/all")
async def fetch_all_ltp():
    symbolList = get_all_symbols_user()
    return await user_symbols_ltp(symbolList)

@symbolRouter.get("/by-market")
def fetch_symbols_by_market(
    market: str = Query(..., description="NSE or BSE")):
    return get_symbols_by_exchange(market)

app.include_router(symbolRouter)