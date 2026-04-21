from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from backend.models.item import Item

async def create_item(session: AsyncSession, item_data: Item):
    db_item = Item.model_validate(item_data)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

async def get_items(session: AsyncSession):
    statement = select(Item)
    result = await session.execute(statement)
    return result.scalars().all()