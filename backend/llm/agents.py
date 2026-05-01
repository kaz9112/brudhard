# agents.py
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from backend.core.vector_db import engine
from backend.core.config import settings
from langgraph.graph import MessagesState
from backend.llm.config import settings
from backend.llm.utils import filter_reasoning_content
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, MessagesState, START, END
from backend.llm.vector_store import vector_store

class State(TypedDict):
    query : list
    doc_vectors: list
    context: str
    item_id: int
    answer: str
    
def build_embedding():
    # Define Node
    workflow = StateGraph(State)
    workflow.add_node("agent", embedding_docs)

    # Define Edge
    workflow.add_edge(START, "agent")
    workflow.add_edge("agent", END)
    return workflow.compile()

def build_answer():
    # Define Node
    workflow = StateGraph(State)
    workflow.add_node("retrieval", embedding_query)
    workflow.add_node("answer", get_answer)

    # Define Edge
    workflow.add_edge(START, "retrieval")
    workflow.add_edge("retrieval", "answer")
    workflow.add_edge("answer", END)
    return workflow.compile()

def get_embeddings_model():
    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=settings.gemini_api_key,
        output_dimensionality=768,
    )

def embedding_docs(state: State):
    embeddings = get_embeddings_model()
    text = state["query"]
    metadatas = {["item_id"]: state["item_id"]} * len(text)
    vector_store.add_texts(
        texts=text,
        metadatas=metadatas,
    )
    return

def embedding_query(state: State):
    query_text = state["query"]
    target_id = state["item_id"]    
    search_filter = {"item_id": target_id}
    docs = vector_store.similarity_search(
        query_text,
        k=2,
        filter=search_filter
    )

    retrieved_context = "\n\n".join([doc.page_content for doc in docs])
    return {"context": retrieved_context}

def get_answer(state: State):
    """
    Primary agent node that calls the LLM and cleans reasoning tags.
    """
    question_with_context = "**CONTEXT:**\n" + state["context"] + "\n\n**Question:**\n" + state["query"]
    llm = get_llm()
    response = llm.invoke(question_with_context)
    clean_response = filter_reasoning_content(response)   
    print(f"clean_response_type: \n{type(clean_response.content)}")
    return {"answer": clean_response.content}


def chat_process(model="gemma-4-26b-a4b-it", temperature=0.7, timeout=60):
    try:
        llm_chat = ChatOpenAI(
            model=model,
            openai_api_key=settings.gemini_api_key,
            openai_api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
            temperature=temperature,
            max_tokens=120,
            timeout=timeout,
        )
        return llm_chat
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e        
    
def get_llm(): 
    return ChatOpenAI(
    # model="gemma-3-27b-it",
    model="gemma-4-26b-a4b-it",
    openai_api_key=settings.gemini_api_key,
    openai_api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    temperature=0.7,
    max_tokens=120,
    timeout=30,
)

def call_model(state: State):
    """
    Primary agent node that calls the LLM and cleans reasoning tags.
    """
    response = llm.invoke(state["messages"])
    # print(response)
    clean_response = filter_reasoning_content(response)   
    return {"messages": [clean_response]}

# def call_model(state: State):
#     """
#     Primary agent node that calls the LLM and cleans reasoning tags.
#     """
#     response = llm.invoke(state["messages"])
#     # print(response)
#     clean_response = filter_reasoning_content(response)   
#     return {"messages": [clean_response]}