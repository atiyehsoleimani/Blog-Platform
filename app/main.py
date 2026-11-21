from fastapi import FastAPI, Depends, APIRouter
from app.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.routes.auth import router as auth_router

app = FastAPI(title="Blog Platform")


@app.get("/health")
def health(db: Session=Depends(get_db)):
    t = text("SELECT 1")
    db.execute(t)
    return {"status": "ok", "database": "ok"}

app.include_router(auth_router)
