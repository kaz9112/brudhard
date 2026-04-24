from sqlmodel import Field, Relationship, SQLModel
from typing import Optional

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    
    # Relationship to link back to QuestionAnswer
    questions: List["QuestionAnswer"] = Relationship(back_populates="item")

class QuestionAnswer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: Optional[str] = None
    answer: Optional[str] = None
    
    # The Foreign Key: points to the 'id' of the Item table
    item_id: int = Field(default=None, foreign_key="item.id")
    
    # Relationship to link back to Item
    item: Optional[Item] = Relationship(back_populates="questions")