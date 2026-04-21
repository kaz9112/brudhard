from fastapi import FastAPI, Depends
from sqlmodel import select
from .models.session import get_session

app = FastAPI(title="Fastapi AI Backend")

@app.get("/health")
def health_check():
    return {"status": "alive"}

@app.get("/db-test")
async def test_db(sesion=Depends(get_session)):
    return {"message": "Database session injected!"}