from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from backend.models.item import *
from sqlalchemy.orm import selectinload

async def create_item(session: AsyncSession, item_data: ItemCreate):
    db_item = Item.model_validate(item_data) 
    
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

async def get_items(session: AsyncSession):
    statement = select(Item) 
    result = await session.execute(statement)
    return result.scalars().all()

async def get_item_by_id(session: AsyncSession, item_id: int):
    # Select the Item where the ID matches
    statement = select(Item).where(Item.id == item_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def create_question_answer(session: AsyncSession, qa_data: QuestionAnswer, item_id: int):
    # 1. Convert the Pydantic model to a dictionary
    data_dict = qa_data.model_dump(exclude={"id", "item_id"})
    
    # 2. Manually unpack the dict and inject the item_id from the URL path
    db_qa = QuestionAnswer(**data_dict, item_id=item_id)
    
    # 3. Save to database
    session.add(db_qa)
    await session.commit()
    await session.refresh(db_qa)
    return db_qa
    
async def get_question_answers_by_item(session: AsyncSession, item_id: int):
    statement = select(QuestionAnswer).where(QuestionAnswer.item_id == item_id)
    result = await session.execute(statement)
    return result.scalars().all()

async def get_question_by_id(session: AsyncSession, question_id: int):  
    # Select the Item where the ID matches
    statement = select(QuestionAnswer).where(QuestionAnswer.id == question_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()
