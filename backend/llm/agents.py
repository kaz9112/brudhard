# agents.py
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from config import settings
from utils import filter_reasoning_content

# Initialize the LLM
llm = ChatOpenAI(
    # model="gemma-3-27b-it",
    model="gemma-4-26b-a4b-it",
    openai_api_key=settings.gemini_api_key,
    openai_api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    temperature=0.7,
    max_tokens=120,
    timeout=30,
)

def call_model(state: MessagesState):
    """
    Primary agent node that calls the LLM and cleans reasoning tags.
    """
    response = llm.invoke(state["messages"])
    print(response)
    clean_response = filter_reasoning_content(response)   
    return {"messages": [clean_response]}