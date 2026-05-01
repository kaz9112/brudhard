from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from backend.models.item import *
from sqlalchemy.orm import selectinload
from backend.llm.llm_main import run_embedding_workflow, run_answer_workflow
from backend.llm.pre_process import split_text
from fastapi import BackgroundTasks

async def create_item(session: AsyncSession, item_data: ItemCreate, background_tasks: BackgroundTasks):
    raw_desc = item_data.description
    db_item = Item.model_validate(item_data)
    session.add(db_item)

    desc = split_text(raw_desc)

    # Flush ensures the DB generates an ID for db_item without finishing the transaction
    await session.flush()

    background_tasks.add_task(run_embedding_workflow, desc, db_item.id)
    
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

async def create_question_answer(session: AsyncSession, qa_data: QuestionAnswer, background_tasks: BackgroundTasks, item_id: int):
    try:
        data_dict = qa_data.model_dump(exclude={"id", "item_id", "answer"})
        db_qa = QuestionAnswer(**data_dict, item_id=item_id, answer="Processing...")

        session.add(db_qa)
        await session.commit()
        await session.refresh(db_qa)

        # Pass the ID to the background task so it knows which row to update later
        background_tasks.add_task(run_answer_workflow, db_qa.id, qa_data.question, item_id)
        
        return db_qa    
    except Exception as e:
        print(f"Unexpected error create_question_answer: {e}")

    
async def get_question_answers_by_item(session: AsyncSession, item_id: int):
    statement = select(QuestionAnswer).where(QuestionAnswer.item_id == item_id)
    result = await session.execute(statement)
    return result.scalars().all()

async def get_question_by_id(session: AsyncSession, question_id: int):  
    # Select the Item where the ID matches
    statement = select(QuestionAnswer).where(QuestionAnswer.id == question_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()
