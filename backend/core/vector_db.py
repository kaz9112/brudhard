import sqlalchemy
from langchain_postgres import PGEngine
from backend.core.config import settings
from langchain_postgres.v2.engine import Column

# Shared engine for the whole app
engine = PGEngine.from_connection_string(settings.DATABASE_URL)
item_id_col = Column(name="item_id", data_type="INTEGER")

async def init_vector_db():
    try:
        # Attempt to create the table
        await engine.ainit_vectorstore_table(
            table_name="embedded_text",
            vector_size=768,
            metadata_columns=[item_id_col],
        )
        print("Vector table created successfully.")
        
    except sqlalchemy.exc.ProgrammingError as e:
        # Check if the error is specifically because the relation exists
        if "already exists" in str(e):
            print("Vector table already exists, skipping creation.")
        else:
            # Re-raise if it's a different database error
            raise e