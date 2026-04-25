from sqlmodel import Field, Relationship, SQLModel, Column, Index
from pgvector.sqlalchemy import Vector
from typing import Optional

# --- BASE SCHEMAS (Common fields) ---
class ItemBase(SQLModel):
    title: str
    description: Optional[str] = None

class QuestionAnswerBase(SQLModel):
    question: Optional[str] = None
    answer: Optional[str] = None

# --- API SCHEMAS (What the user sends/receives) ---
class ItemCreate(ItemBase):
    """Schema for creating an item (No ID needed)"""
    pass

class ItemRead(ItemBase):
    """Schema for returning an item (Includes ID)"""
    id: int

class QuestionAnswerCreate(QuestionAnswerBase):
    """What the frontend sends in the JSON body (No ID, No item_id)"""
    pass

class QuestionAnswerRead(QuestionAnswerBase):
    """What the API returns to the frontend (Includes IDs)"""
    id: int
    item_id: int

# --- DATABASE MODELS (The actual tables) ---

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None

    embedding: Optional[list[float]] = Field(
        default=None,
        sa_column=Column(Vector(768)) 
    )

    # Relationship to link back to QuestionAnswer
    questions: list["QuestionAnswer"] = Relationship(back_populates="item")

    __table_args__ = (
        Index(
            "ix_item_embedding",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )



class QuestionAnswer(QuestionAnswerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: Optional[str] = None
    answer: Optional[str] = None
    
    # The Foreign Key: points to the 'id' of the Item table
    item_id: int = Field(default=None, foreign_key="item.id")
    
    # Relationship to link back to Item
    item: Optional[Item] = Relationship(back_populates="questions")