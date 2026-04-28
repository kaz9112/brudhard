# agents.py
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.graph import MessagesState
from backend.llm.config import settings
from backend.llm.utils import filter_reasoning_content
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, MessagesState, START, END


class State(TypedDict):
    query : str
    doc_vectors: list
    

def build_embedding():
    # Define Node
    workflow = StateGraph(State)
    workflow.add_node("agent", embedding_docs)

    # Define Edge
    workflow.add_edge(START, "agent")
    workflow.add_edge("agent", END)
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
    doc_vectors = embeddings.embed_documents([text])

    return {"doc_vectors": doc_vectors}

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
    
llm = ChatOpenAI(
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

def call_model(state: State):
    """
    Primary agent node that calls the LLM and cleans reasoning tags.
    """
    response = llm.invoke(state["messages"])
    # print(response)
    clean_response = filter_reasoning_content(response)   
    return {"messages": [clean_response]}