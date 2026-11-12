from fastapi import FastAPI, Depends
from app.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session

app = FastAPI(title="Blog Platform")


@app.get("/health")
def health(db: Session=Depends(get_db)):
    t = text("SELECT 1")
    db.execute(t)
    return {"status": "ok", "database": "ok"}
