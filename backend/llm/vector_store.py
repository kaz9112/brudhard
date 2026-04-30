import sqlalchemy
from langchain_postgres import PGVectorStore
from langchain_postgres.v2.indexes import HNSWIndex
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.core.vector_db import engine
from backend.llm.config import settings

def get_embeddings_model():
    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=settings.gemini_api_key,
        output_dimensionality=768,
    )

vector_store = PGVectorStore.create_sync(
    engine=engine,
    embedding_service=get_embeddings_model(),
    table_name="embedded_text", 
    metadata_columns=["item_id"],
)

# To use HNSW (Recommended for most RAG apps)
async def ensure_vector_indices():
    try:
        # We define the index
        hnsw_index = HNSWIndex()
        
        # Attempt to apply it
        await vector_store.aapply_vector_index(hnsw_index)
        print("Vector index created successfully.")
        
    except sqlalchemy.exc.ProgrammingError as e:
        # Check if the error is because the index already exists
        if "already exists" in str(e).lower():
            print("Vector index already exists, skipping creation.")
        else:
            # Re-raise if it's a different database error
            raise e
    except Exception as e:
        print(f"Unexpected error creating index: {e}")

# # OR to use IVFFlat
# ivfflat_index = IVFFlatIndex()
# await vector_store.aapply_vector_index(ivfflat_index)