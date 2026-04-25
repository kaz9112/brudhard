from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.session import get_session
from backend.models.item import *
from backend.crud import item as crud_item
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fastapi AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "alive"}

# @app.get("/db-test")
# async def test_db(sesion=Depends(get_session)):
#     return {"message": "Database session injected!"}

@app.post("/items", response_model=ItemRead)
async def create_new_item(item: ItemCreate, db: AsyncSession = Depends(get_session)):
    return await crud_item.create_item(db, item)

@app.get("/items", response_model=list[ItemRead])
async def read_items(db: AsyncSession = Depends(get_session)):
    return await crud_item.get_items(db)

@app.post("/items/{item_id}/questions", response_model=QuestionAnswerRead)
async def create_new_question(
    item_id: int, 
    qa_in: QuestionAnswerCreate,
    session: AsyncSession = Depends(get_session)
):
    return await crud_item.create_question_answer(session, qa_in, item_id)

@app.get("/items/{item_id}/questions", response_model=list[QuestionAnswerRead])
async def read_questions_for_item(
    item_id: int,
    db: AsyncSession = Depends(get_session)
):
    # Pass the item_id to filter the questions
    return await crud_item.get_question_answers_by_item(db, item_id)