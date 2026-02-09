# services/auth_service/app/main.py
from fastapi import FastAPI, HTTPException
from angel_auth import angel_login

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

