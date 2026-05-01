from backend.llm.agents import call_model, embedding_docs, build_embedding, build_answer
from backend.models.session import async_session
from backend.models.item import QuestionAnswer
from sqlalchemy import update

# Compile the app instance once at the module level
def run_embedding_workflow(query: list, item_id: int) -> list:
    """
    Entry point for external services (like Celery).
    Takes a string, runs the graph, and returns the final AI response string.
    """
    app = build_embedding()
    inputs = {"query": query, "item_id": item_id}
    
    app.invoke(inputs)
    return

async def run_answer_workflow(qa_id: int, query: str, item_id: int) -> list:
    """
    Entry point for external services (like Celery).
    Takes a string, runs the graph, and returns the final AI response string.
    """
    app = build_answer()
    inputs = {"query": query, "item_id": item_id}
    
    result = await app.ainvoke(inputs)
    # Extract the content of the last message (the AI's response)
    final_answer = result["answer"]

    async with async_session() as session:
            async with session.begin():
                stmt = (
                    update(QuestionAnswer)
                    .where(QuestionAnswer.id == qa_id)
                    .values(answer=final_answer)
                )
                await session.execute(stmt)

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