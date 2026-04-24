from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from backend.models.item import Item, QuestionAnswer
from sqlalchemy.orm import selectinload

async def create_item(session: AsyncSession, item_data: Item):
    session.add(item_data)
    await session.commit()
    await session.refresh(item_data)
    return item_data

async def get_items(session: AsyncSession):
    statement = select(Item)
    result = await session.execute(statement)
    return result.scalars().all()

async def create_question_answer(session: AsyncSession, qa_data: QuestionAnswer, item_id: int):
    # 1. Convert the Pydantic model to a dictionary
    # We exclude 'item_id' from the dict so it doesn't overwrite our path variable
    data_dict = qa_data.model_dump(exclude={"id", "item_id"})
    
    # 2. Manually unpack the dict and inject the item_id from the URL path
    db_qa = QuestionAnswer(**data_dict, item_id=item_id)
    
    # 3. Save to database
    session.add(db_qa)
    await session.commit()
    await session.refresh(db_qa)
    return db_qa
    
async def get_question_answers_by_item(session: AsyncSession, item_id: int):
    # Filter the select statement so you only get QAs for this specific item
    statement = select(QuestionAnswer).where(QuestionAnswer.item_id == item_id)
    result = await session.execute(statement)
    return result.scalars().all()