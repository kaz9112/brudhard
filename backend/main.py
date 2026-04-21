from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.session import get_session
from backend.models.item import Item
from backend.crud import item as crud_item
app = FastAPI(title="Fastapi AI Backend")

@app.get("/health")
def health_check():
    return {"status": "alive"}

# @app.get("/db-test")
# async def test_db(sesion=Depends(get_session)):
#     return {"message": "Database session injected!"}

@app.post("/items", response_model=Item)
async def create_new_item(item: Item, db: AsyncSession = Depends(get_session)):
    return await crud_item.create_item(db, item)

@app.get("/items", response_model=list[Item])
async def read_items(db: AsyncSession = Depends(get_session)):
    return await crud_item.get_items(db)