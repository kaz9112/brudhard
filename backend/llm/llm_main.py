# main.py
from backend.llm.agents import call_model, embedding_docs, build_embedding

# def build_graph():
#     # Define Node
#     workflow = StateGraph(MessagesState)
#     workflow.add_node("agent", call_model)

#     # Define Edge
#     workflow.add_edge(START, "agent")
#     workflow.add_edge("agent", END)
#     return workflow.compile()
 


# Compile the app instance once at the module level

def run_embedding_workflow(query: str) -> list:
    """
    Entry point for external services (like Celery).
    Takes a string, runs the graph, and returns the final AI response string.
    """
    app = build_embedding()
    inputs = {"query": query}
    
    # Use .invoke() for a single synchronous result, or 
    # iterate through .stream() to get the final state.
    # .invoke() is usually cleaner for task-based processing.
    result = app.invoke(inputs)
    
    # Extract the content of the last message (the AI's response)
    last_msg = result["doc_vectors"][-1]
    return last_msg

# def run_agent_workflow(query: str) -> str:
#     """
#     Entry point for external services (like Celery).
#     Takes a string, runs the graph, and returns the final AI response string.
#     """
#     app = build_graph()
#     inputs = {"query": query}
    
#     # Use .invoke() for a single synchronous result, or 
#     # iterate through .stream() to get the final state.
#     # .invoke() is usually cleaner for task-based processing.
#     result = app.invoke(inputs)
    
#     # Extract the content of the last message (the AI's response)
#     last_msg = result["doc_vectors"][-1]
#     return last_msg


if __name__ == "__main__":
    # Local testing
    print("--- Running Local Test ---")
    response = run_agent_workflow("8 x 18 - 345 / 5.32 =")
    # print(f"Final Result: {response}")